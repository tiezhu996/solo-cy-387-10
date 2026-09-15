import { auth, clearAuth } from '../stores/auth';
import type {
  Booking,
  FavoriteItem,
  FavoriteState,
  LoginResult,
  PropertyItem,
  RepairTicket,
  UserInfo,
} from '../types/domain';

const API_BASE = '/api';

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  if (auth.token) headers.Authorization = `Bearer ${auth.token}`;
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

export async function login(username: string, password: string): Promise<LoginResult> {
  return request<LoginResult>('/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  });
}

export async function getMe(): Promise<UserInfo> {
  return request<UserInfo>('/auth/me/');
}

export async function getProperties(): Promise<PropertyItem[]> {
  return request<PropertyItem[]>('/properties/');
}

export async function getProperty(id: number): Promise<PropertyItem> {
  return request<PropertyItem>(`/properties/${id}/`);
}

export async function delistProperty(id: number): Promise<PropertyItem> {
  return request<PropertyItem>(`/properties/${id}/delist/`, { method: 'POST' });
}

export async function getFavorites(): Promise<FavoriteItem[]> {
  return request<FavoriteItem[]>('/favorites/');
}

/** 幂等设置收藏状态，返回服务端最终状态与收藏数。 */
export async function setFavorite(propertyId: number, favorite: boolean): Promise<FavoriteState> {
  return request<FavoriteState>(`/favorites/${propertyId}/`, {
    method: 'PUT',
    body: JSON.stringify({ favorite }),
  });
}

export async function createBooking(propertyId: number, slot: string): Promise<Booking> {
  return request<Booking>('/bookings/', {
    method: 'POST',
    body: JSON.stringify({ propertyId, slot }),
  });
}

export async function createRepair(ticket: Pick<RepairTicket, 'faultType' | 'description'>): Promise<RepairTicket> {
  return request<RepairTicket>('/repairs/', {
    method: 'POST',
    body: JSON.stringify(ticket),
  });
}
