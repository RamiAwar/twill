export interface ClientError {
  // Error
  message: string;
  code?: number;
  id: number;

  // Banner properties
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
