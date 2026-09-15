#!/usr/bin/env python3
"""房源列表与收藏夹并发竞争集成测试。

设计约束：
- 真实持久化请求：启动独立 runserver 子进程 + 独立测试数据库，
  所有竞争操作走真实 HTTP API，不使用进程内假数据、请求桩；
  每个请求都是独立 TCP 连接，读写线程真正并发，不做串行化。
- 竞争结构：账号 A 的写线程对若干房源反复收藏/取消，
  账号 A 与账号 B 两个读线程同时持续读取房源列表与收藏夹。
- 断言：任意时刻响应内的收藏总数与个人状态自洽，写完后最终关系精确匹配。
- 失败报告包含：读取阶段、账号、可见结果与期望约束。
- 覆盖空数据集；测试数据自行清理，可连续重复运行。

运行方式：
    python backend/tests/race_test.py
默认使用临时 sqlite（WAL 模式）；设置 RACE_DATABASE_URL 可对 PostgreSQL 运行：
    RACE_DATABASE_URL=postgres://user:pass@host:5432/db python backend/tests/race_test.py
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROPERTY_COUNT = 5          # 竞争用房源数量
WRITE_ROUNDS = 40           # 写线程反复收藏/取消的轮数
MAX_REPORTED_FAILURES = 20  # 失败详情最多打印条数

# ---------------------------------------------------------------------------
# 失败收集：每条失败都记录读取阶段、账号、可见结果与期望约束
# ---------------------------------------------------------------------------
_failures = []
_fail_lock = threading.Lock()
_stats = {'reads': 0, 'writes': 0, 'checks': 0}


def record_failure(phase: str, account: str, visible, expect: str):
    with _fail_lock:
        _failures.append({'phase': phase, 'account': account, 'visible': visible, 'expect': expect})


def bump(counter: str, amount: int = 1):
    with _fail_lock:
        _stats[counter] += amount


# ---------------------------------------------------------------------------
# HTTP 辅助：无共享连接、无缓存，每次请求都是新的 TCP 连接
# ---------------------------------------------------------------------------
def http(method: str, base: str, path: str, token: str = None, body=None):
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(base + path, method=method, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode() or 'null')
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            return exc.code, json.loads(raw or 'null')
        except json.JSONDecodeError:
            return exc.code, raw


def login(base: str, username: str) -> str:
    status, data = http('POST', base, '/api/auth/login/', body={'username': username, 'password': '123456'})
    if status != 200:
        raise RuntimeError(f'登录失败 {username}: {status} {data}')
    return data['token']


# ---------------------------------------------------------------------------
# 不变量断言：对每一次读响应逐条校验，失败时记录阶段/账号/可见结果
# ---------------------------------------------------------------------------
def check_list_response(phase: str, account: str, only_writer_favorites: bool, data, test_ids: set):
    """列表响应内部自洽：favorited 与 favoriteCount 必须互相印证。

    竞争期间只有账号 A 会收藏测试房源，因此测试房源的 favoriteCount 恒 ∈ {0,1}：
    - 读账号是 A 自己：favorited=True 时计数必须恰为 1，False 时必须恰为 0；
    - 读账号是 B：favorited 恒为 False，计数恒 ∈ {0,1}（不能重复计数）。
    """
    by_id = {p['id']: p for p in data}
    for pid in test_ids:
        p = by_id.get(pid)
        if p is None:
            record_failure(phase, account, {'propertyId': pid, 'visible': '列表中缺失'}, '测试房源必须出现在列表中')
            continue
        bump('checks')
        count, favorited = p['favoriteCount'], p['favorited']
        if count not in (0, 1):
            record_failure(phase, account, p, '竞争期间 favoriteCount 只能为 0 或 1（唯一约束，不得重复计数）')
        if only_writer_favorites:
            if favorited and count != 1:
                record_failure(phase, account, p, '本人已收藏时 favoriteCount 必须为 1')
            if not favorited and count != 0:
                record_failure(phase, account, p, '本人未收藏时 favoriteCount 必须为 0（唯一收藏者只有本账号）')
        else:
            if favorited:
                record_failure(phase, account, p, '未参与收藏的账号 favorited 必须恒为 False')


def check_favorites_response(phase: str, account: str, is_writer: bool, data, test_ids: set):
    """收藏夹响应内部自洽：条目都属于本账号且状态有效。"""
    if not isinstance(data, list):
        record_failure(phase, account, data, '收藏夹响应必须是数组')
        return
    bump('checks')
    if not is_writer and len(data) != 0:
        record_failure(phase, account, data, '未参与收藏的账号收藏夹必须恒为空')
        return
    if len(data) > len(test_ids):
        record_failure(phase, account, f'共 {len(data)} 条', f'收藏夹条数不得超过测试房源数 {len(test_ids)}（不得重复收藏）')
    seen = set()
    for entry in data:
        pid = entry.get('propertyId')
        if pid in seen:
            record_failure(phase, account, entry, '收藏夹中同一房源不得出现两次')
        seen.add(pid)
        if pid not in test_ids:
            record_failure(phase, account, entry, '收藏夹只应包含本账号收藏的测试房源')
            continue
        prop = entry.get('property') or {}
        if entry.get('valid') is not True:
            record_failure(phase, account, entry, '在租测试房源的收藏必须有效（valid=True）')
        if prop.get('favorited') is not True:
            record_failure(phase, account, entry, '收藏夹条目对本账号 favorited 必须为 True')
        if prop.get('favoriteCount') != 1:
            record_failure(phase, account, entry, '收藏夹条目 favoriteCount 必须为 1（唯一收藏者）')


# ---------------------------------------------------------------------------
# 竞争线程
# ---------------------------------------------------------------------------
def writer_thread(base: str, token: str, test_ids: list, stop: threading.Event):
    """账号 A：对每套房源反复收藏/取消，最后一轮留下确定的最终状态。"""
    account = 'race_tenant_a'
    for round_no in range(WRITE_ROUNDS):
        if stop.is_set():
            return
        for idx, pid in enumerate(test_ids):
            favorite = (round_no + idx) % 2 == 0
            status, data = http('PUT', base, f'/api/favorites/{pid}/', token=token, body={'favorite': favorite})
            bump('writes')
            if status != 200:
                record_failure('竞争写入', account, {'status': status, 'body': data}, '写入必须全部成功')
    # 最终一轮：偶数下标收藏、奇数下标取消，形成确定的最终关系
    for idx, pid in enumerate(test_ids):
        status, data = http('PUT', base, f'/api/favorites/{pid}/', token=token, body={'favorite': idx % 2 == 0})
        bump('writes')
        if status != 200:
            record_failure('最终写入', account, {'status': status, 'body': data}, '最终状态写入必须成功')


def reader_thread(base: str, token: str, account: str, is_writer_account: bool,
                  test_ids: set, stop: threading.Event):
    """读线程：持续读取列表与收藏夹，对每次响应校验不变量。"""
    while not stop.is_set():
        status, data = http('GET', base, '/api/properties/', token=token)
        bump('reads')
        if status != 200:
            record_failure('竞争读取-列表', account, {'status': status, 'body': data}, '读取必须成功')
        else:
            check_list_response('竞争读取-列表', account, is_writer_account, data, test_ids)

        status, data = http('GET', base, '/api/favorites/', token=token)
        bump('reads')
        if status != 200:
            record_failure('竞争读取-收藏夹', account, {'status': status, 'body': data}, '读取必须成功')
        else:
            check_favorites_response('竞争读取-收藏夹', account, is_writer_account, data, test_ids)
        time.sleep(0.005)


# ---------------------------------------------------------------------------
# 环境搭建 / 清理
# ---------------------------------------------------------------------------
def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


def run_migrate(env):
    result = subprocess.run(
        [sys.executable, 'manage.py', 'migrate', '--noinput'],
        cwd=BACKEND_DIR, env=env, capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError('测试数据库迁移失败')


def enable_wal_if_sqlite(db_url: str):
    """sqlite 开启 WAL：读写不互斥，竞争是真实并发而非串行连接。"""
    if not db_url.startswith('sqlite'):
        return
    import sqlite3
    db_path = db_url.split('///', 1)[-1]
    with sqlite3.connect(db_path) as conn:
        conn.execute('PRAGMA journal_mode=WAL;')


def django_shell(env, statement: str):
    """在测试数据库上执行 ORM 语句（仅用于夹具搭建与清理，不在竞争路径上）。"""
    result = subprocess.run(
        [sys.executable, 'manage.py', 'shell', '-c', statement],
        cwd=BACKEND_DIR, env=env, capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError(f'ORM 操作失败: {statement[:60]}')


def setup_fixtures(env):
    django_shell(env, """
from django.contrib.auth import get_user_model
from app.apps.users.models import Profile
User = get_user_model()
User.objects.filter(username__startswith='race_').delete()
for name, role in [('race_tenant_a', '租客'), ('race_tenant_b', '租客'), ('race_landlord', '房东')]:
    user = User.objects.create_user(username=name, password='123456')
    Profile.objects.create(user=user, role=role)
print('fixtures ready')
""")


def cleanup_fixtures(env):
    django_shell(env, """
from django.contrib.auth import get_user_model
from app.apps.properties.models import Property
User = get_user_model()
User.objects.filter(username__startswith='race_').delete()  # 级联删除其房源与收藏
leftover_users = User.objects.filter(username__startswith='race_').count()
leftover_props = Property.objects.filter(community__startswith='竞争测试房源').count()
assert leftover_users == 0 and leftover_props == 0, f'清理残留: users={leftover_users} props={leftover_props}'
print('cleanup verified')
""")


def wait_ready(base: str, timeout: float = 30.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            status, _ = http('GET', base, '/api/properties/')
            if status == 200:
                return
        except (urllib.error.URLError, ConnectionError, OSError):
            pass
        time.sleep(0.3)
    raise RuntimeError('测试服务器启动超时')


# ---------------------------------------------------------------------------
# 测试主体
# ---------------------------------------------------------------------------
def run_suite(base: str):
    token_a = login(base, 'race_tenant_a')
    token_b = login(base, 'race_tenant_b')
    token_landlord = login(base, 'race_landlord')

    # ---- 空数据集覆盖 ----
    status, data = http('GET', base, '/api/favorites/', token=token_b)
    bump('checks')
    if status != 200 or data != []:
        record_failure('空数据-收藏夹', 'race_tenant_b', {'status': status, 'body': data}, '空收藏夹必须返回 200 与 []')
    status, data = http('GET', base, '/api/properties/?region=' + urllib.parse.quote('不存在区域'), token=token_a)
    bump('checks')
    if status != 200 or data != []:
        record_failure('空数据-列表筛选', 'race_tenant_a', {'status': status, 'body': data}, '无匹配筛选必须返回 200 与 []')

    # ---- 构造竞争房源（真实 API 发布，归属 race_landlord）----
    test_ids = []
    for idx in range(PROPERTY_COUNT):
        body = {
            'community': f'竞争测试房源{idx}', 'region': '滨江区', 'layout': '一室一厅',
            'area': 50, 'rent': 4000, 'deposit': 4000, 'payment': '月付',
            'facilities': ['空调'], 'description': '竞争测试', 'photos': [],
            'landlordPhone': '13900000000',
        }
        status, data = http('POST', base, '/api/properties/', token=token_landlord, body=body)
        if status != 201:
            record_failure('夹具搭建', 'race_landlord', {'status': status, 'body': data}, '发布测试房源必须成功')
            raise RuntimeError('无法创建测试房源')
        test_ids.append(data['id'])
    test_id_set = set(test_ids)

    # ---- 竞争阶段：1 个写线程 + 2 个读线程真正并发 ----
    stop = threading.Event()
    threads = [
        threading.Thread(target=writer_thread, args=(base, token_a, test_ids, stop), name='writer'),
        threading.Thread(target=reader_thread, args=(base, token_a, 'race_tenant_a', True, test_id_set, stop), name='reader-a'),
        threading.Thread(target=reader_thread, args=(base, token_b, 'race_tenant_b', False, test_id_set, stop), name='reader-b'),
    ]
    for thread in threads:
        thread.start()
    threads[0].join()          # 等写线程完成全部轮次与最终一轮
    stop.set()
    for thread in threads[1:]:
        thread.join()

    # ---- 最终关系校验：偶数下标收藏、奇数下标未收藏 ----
    expected = {pid: (idx % 2 == 0) for idx, pid in enumerate(test_ids)}

    status, data = http('GET', base, '/api/favorites/', token=token_a)
    final_ids = {entry['propertyId'] for entry in data} if isinstance(data, list) else set()
    expected_ids = {pid for pid, fav in expected.items() if fav}
    if status != 200 or final_ids != expected_ids:
        record_failure('最终校验-收藏夹', 'race_tenant_a', {'status': status, 'visible': sorted(final_ids)},
                       f'最终收藏关系必须精确等于 {sorted(expected_ids)}')

    status, data = http('GET', base, '/api/properties/', token=token_a)
    by_id = {p['id']: p for p in data} if isinstance(data, list) else {}
    for pid, fav in expected.items():
        p = by_id.get(pid)
        if p is None:
            record_failure('最终校验-列表', 'race_tenant_a', {'propertyId': pid}, '测试房源必须仍在列表中')
            continue
        bump('checks')
        if p['favorited'] != fav or p['favoriteCount'] != (1 if fav else 0):
            record_failure('最终校验-列表', 'race_tenant_a', p,
                           f'最终状态应为 favorited={fav}, favoriteCount={1 if fav else 0}')

    status, data = http('GET', base, '/api/properties/', token=token_b)
    by_id = {p['id']: p for p in data} if isinstance(data, list) else {}
    for pid, fav in expected.items():
        p = by_id.get(pid)
        if p is None:
            continue
        bump('checks')
        if p['favorited'] is not False or p['favoriteCount'] != (1 if fav else 0):
            record_failure('最终校验-列表', 'race_tenant_b', p,
                           f'账号 B 视角应为 favorited=False, favoriteCount={1 if fav else 0}')

    status, data = http('GET', base, '/api/favorites/', token=token_b)
    if status != 200 or data != []:
        record_failure('最终校验-收藏夹', 'race_tenant_b', {'status': status, 'body': data}, '账号 B 收藏夹必须为空')


def main() -> int:
    port = free_port()
    base = f'http://127.0.0.1:{port}'
    tmp_dir = tempfile.mkdtemp(prefix='rentfind_race_')
    db_url = os.environ.get('RACE_DATABASE_URL') or f'sqlite:///{tmp_dir}/db.sqlite3'

    env = os.environ.copy()
    env['DATABASE_URL'] = db_url
    env['DJANGO_SECRET_KEY'] = 'race-test-secret'
    env['PYTHONPATH'] = str(BACKEND_DIR)

    server = None
    log_path = Path(tmp_dir) / 'server.log'
    try:
        print(f'[setup] 数据库: {db_url}')
        run_migrate(env)
        enable_wal_if_sqlite(db_url)
        setup_fixtures(env)

        print(f'[setup] 启动测试服务器 {base}')
        with open(log_path, 'w') as log:
            server = subprocess.Popen(
                [sys.executable, 'manage.py', 'runserver', f'127.0.0.1:{port}', '--noreload'],
                cwd=BACKEND_DIR, env=env, stdout=log, stderr=subprocess.STDOUT,
            )
        wait_ready(base)

        print(f'[race] 写线程 {WRITE_ROUNDS} 轮 x {PROPERTY_COUNT} 套房源，2 个读线程持续读取')
        try:
            run_suite(base)
        except Exception as exc:  # noqa: BLE001 — 夹具/网络异常也走统一失败报告
            record_failure('执行', 'harness', repr(exc), '测试套件必须正常执行完成')
    finally:
        if server is not None:
            server.terminate()
            try:
                server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                server.kill()
        log_tail = ''
        try:
            log_tail = log_path.read_text()[-3000:]
        except OSError:
            pass
        try:
            cleanup_fixtures(env)
            print('[cleanup] 测试数据已清理并校验无残留')
        except Exception as exc:  # noqa: BLE001
            record_failure('清理', 'harness', str(exc), '测试数据必须清理干净')
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"[stats] 读请求 {_stats['reads']} 次，写请求 {_stats['writes']} 次，不变量校验 {_stats['checks']} 次")
    if _failures:
        print(f'\n[FAILED] 共 {len(_failures)} 处失败（最多展示 {MAX_REPORTED_FAILURES} 条）:')
        for failure in _failures[:MAX_REPORTED_FAILURES]:
            print(f"  阶段={failure['phase']} 账号={failure['account']}")
            print(f"    可见结果: {json.dumps(failure['visible'], ensure_ascii=False)[:400]}")
            print(f"    期望约束: {failure['expect']}")
        if log_tail:
            print('\n服务器日志尾部:')
            print(log_tail)
        return 1
    print('[OK] 全部通过')
    return 0


if __name__ == '__main__':
    sys.exit(main())
