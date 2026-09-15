import { auth, clearAuth } from '../stores/auth';
const API_BASE = '/api';
async function request(path, options = {}) {
    const headers = { 'Content-Type': 'application/json' };
    if (auth.token)
        headers.Authorization = `Bearer ${auth.token}`;
    const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
    if (response.status === 401) {
        clearAuth();
        throw new Error('登录已失效，请重新登录');
    }
    if (!response.ok) {
        const data = await response.json().catch(() => null);
        const message = data?.error?.message ?? data?.error?.detail ?? '请求失败，请稍后重试';
        throw new Error(typeof message === 'string' ? message : '请求失败，请稍后重试');
    }
    return response.json();
}
export async function login(username, password) {
    return request('/auth/login/', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
    });
}
export async function getMe() {
    return request('/auth/me/');
}
export async function getProperties() {
    return request('/properties/');
}
export async function getProperty(id) {
    return request(`/properties/${id}/`);
}
export async function delistProperty(id) {
    return request(`/properties/${id}/delist/`, { method: 'POST' });
}
export async function getFavorites() {
    return request('/favorites/');
}
/** 幂等设置收藏状态，返回服务端最终状态与收藏数。 */
export async function setFavorite(propertyId, favorite) {
    return request(`/favorites/${propertyId}/`, {
        method: 'PUT',
        body: JSON.stringify({ favorite }),
    });
}
export async function createBooking(propertyId, slot) {
    return request('/bookings/', {
        method: 'POST',
        body: JSON.stringify({ propertyId, slot }),
    });
}
export async function createRepair(ticket) {
    return request('/repairs/', {
        method: 'POST',
        body: JSON.stringify(ticket),
    });
}
