import { reactive } from 'vue';
import type { UserInfo } from '../types/domain';

const TOKEN_KEY = 'rentfind_token';
const USER_KEY = 'rentfind_user';

function loadUser(): UserInfo | null {
  try {
    const raw = localStorage.getItem(USER_KEY);
    return raw ? (JSON.parse(raw) as UserInfo) : null;
  } catch {
    return null;
  }
}

/** 全局登录态：token 与用户信息持久化在 localStorage，刷新后自动恢复。 */
export const auth = reactive({
  token: localStorage.getItem(TOKEN_KEY) ?? '',
  user: loadUser(),
});

export function setAuth(token: string, user: UserInfo) {
  auth.token = token;
  auth.user = user;
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, JSON.stringify(user));
}

export function clearAuth() {
  auth.token = '';
  auth.user = null;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}
