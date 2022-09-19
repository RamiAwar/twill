export interface ClientError {
  // Error
  message: string;
  code?: number;
  id: number;

  // Banner properties
  dismissable?: boolean;
  ephemeral?: boolean;
  timeout?: number;
}
