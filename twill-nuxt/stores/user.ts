import { defineStore } from "pinia";
import { UserAuthResponse } from "@/models/auth";

export const useUserStore = defineStore("user", {
  state(): UserAuthResponse {
    return {
      id: null,
      name: null,
      profile_image_url: null,
      twitter_handle: null,
      twitter_followers_count: null,
    };
  },
  getters: {
    isLoggedIn(): boolean {
      return this.id !== null;
    },
  },
  actions: {
    logout(): void {
      this.id = null;
      this.name = null;
      this.profile_image_url = null;
      this.twitter_handle = null;
      this.twitter_followers_count = null;
    },
  },
  persist: true,
});
