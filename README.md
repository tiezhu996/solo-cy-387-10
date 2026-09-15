# RentFind 租房与物业报修平台

```bash
cp .env.example .env
docker compose up -d --build
```

RentFind 面向房东、租客和物业人员，提供房源发布、搜索预约、房源详情、收藏夹、合同管理和报修跟踪能力。

## 项目主要功能

- 房源发布：小区、户型、面积、租金、押金、付款方式、照片和设施。
- 搜索筛选：区域、价格、户型、面积、设施，并支持列表和地图视图切换。
- 房源详情：照片轮播、详细描述、配套设施清单、房东联系方式。
- 收藏夹：租客登录后可收藏/取消收藏，按账号隔离，刷新或重新登录后保留；房东下架房源后收藏立即标记失效且不可预约；重复点击幂等，不会产生重复记录或计数错乱。
- 预约看房：租客选择时间段，房东确认后生成通知；已下架房源禁止预约。
- 合同管理：生成租赁合同模板并记录租期、租金、双方信息和状态。
- 物业报修：提交故障类型、描述和照片，物业接单并更新进度。
- 角色区分：房东、租客、物业人员拥有不同工作台。

## 快速启动方式

首次启动前执行：

```bash
cp .env.example .env
docker compose up -d --build
```

访问地址：http://localhost:18407

演示账号（密码均为 `123456`）：

| 账号 | 角色 |
| --- | --- |
| tenant1 / tenant2 | 租客 |
| landlord1 | 房东 |
| worker1 | 物业人员 |

## 本地开发方式

```bash
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
cd frontend && npm install && npm run dev
```

## 技术栈

| 模块 | 技术 |
| --- | --- |
| 前端 | Vue 3、TypeScript、Element Plus、Vue Router、Vite、高德地图 JS API |
| 后端 | Python、Django、Django REST Framework、SimpleJWT |
| 数据库 | PostgreSQL |
| 认证 | JWT |
| 部署 | Docker Compose、Nginx |

## 项目目录结构

```text
.
├── backend
│   ├── app
│   │   ├── apps
│   │   │   ├── users        # 用户与 JWT 登录
│   │   │   ├── properties   # 房源列表/详情/下架
│   │   │   ├── favorites    # 收藏夹（幂等写、按用户隔离）
│   │   │   ├── booking      # 预约看房
│   │   │   ├── contract     # 合同
│   │   │   └── repair       # 报修
│   │   ├── constants        # 枚举与错误码
│   │   ├── middleware
│   │   ├── utils
│   │   └── settings.py
│   ├── database
│   └── manage.py
├── frontend
│   ├── src
│   │   ├── api              # API 请求（自动携带 JWT）
│   │   ├── router           # 路由与登录守卫
│   │   ├── stores           # 登录态（localStorage 持久化）
│   │   ├── views            # 列表/详情/收藏夹/登录页
│   │   └── components
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## 环境变量说明

| 变量 | 说明 |
| --- | --- |
| COMPOSE_PROJECT_NAME | Compose 项目名，固定为 rentfind |
| POSTGRES_DB / POSTGRES_USER / POSTGRES_PASSWORD | PostgreSQL 数据库、账号、密码 |
| DATABASE_URL | Django 连接 PostgreSQL 的地址 |
| DJANGO_SECRET_KEY | Django 密钥 |
| DJANGO_DEBUG | 是否开启调试模式 |
| AMAP_KEY | 高德地图 JS API Key |

## Docker 部署说明

Compose 顶层声明 `name: rentfind`，容器名带 `rentfind-` 前缀，数据库和媒体文件分别使用命名卷持久化，前端 Nginx 将 `/api` 代理到后端 `backend:8000`。后端容器启动时自动执行 `manage.py migrate` 完成建表与演示数据初始化。

## License

MIT
