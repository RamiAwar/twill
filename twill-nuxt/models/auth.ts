export interface LoginRedirect {
  redirect_url: string;
}

export interface UserAuthResponse {
  id: string;
  name: string;
  profile_image_url: string;
  twitter_handle: string;
  twitter_followers_count: number;
}
