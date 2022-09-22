export enum BannerType {
  Error = "error",
  Warning = "warning",
  Info = "info",
  Success = "success",
}

export interface BannerResponse {
  message: string;
  type: BannerType;
}

export interface Banner {
  // Error
  message: string;
  code?: number;
  id: number;

  // Banner properties
  type: BannerType;
  dismissable?: boolean;
  ephemeral?: boolean;
  timeout?: number;

  // Optional
  meta?: string;
  link?: string;
}

export interface APIError {
  message: string;
  code?: number;
}

export interface APIResponse<T> {
  body: T;
  error: APIError;
}
