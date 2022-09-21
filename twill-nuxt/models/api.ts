import { APIError } from "@/models/error";

export interface APIResponse<T> {
  body: T;
  error: APIError;
}
