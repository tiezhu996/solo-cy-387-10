export interface PropertyItem {
  id: number;
  landlordId: number;
  community: string;
  region: string;
  layout: string;
  area: number;
  rent: number;
  deposit: number;
  payment: string;
  facilities: string[];
  description: string;
  photos: string[];
  status: string;
  landlordPhone: string;
  favoriteCount: number;
  favorited: boolean;
  bookable: boolean;
}

export interface FavoriteItem {
  id: number;
  propertyId: number;
  property: PropertyItem;
  valid: boolean;
  createdAt: string;
}

export interface UserInfo {
  id: number;
  username: string;
  role: string;
}

export interface LoginResult {
  token: string;
  user: UserInfo;
}

export interface FavoriteState {
  propertyId: number;
  favorited: boolean;
  favoriteCount: number;
}

export interface RepairTicket {
  id: number;
  faultType: string;
  description: string;
  status: string;
}

export interface Booking {
  id: number;
  propertyId?: number;
  status: string;
  slot: string;
}
