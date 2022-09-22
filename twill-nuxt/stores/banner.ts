import { defineStore } from "pinia";
import { Banner, BannerType, BannerResponse } from "@/models/api";
import routes from "@/routes";

function handleErrorCode(error: Banner) {
  switch (error.code) {
    case 412:
      error.meta = "Signup for beta";
      error.link = routes.beta_signup;
      return error;
    case 422:
      error.message = "Something went wrong! Please try again later.";
      return error;
    default:
      return error;
  }
}

export const useBannerStore = defineStore("banner", {
  state() {
    return {
      counter: 0,
      banners: [] as Banner[],
    };
  },
  getters: {},
  actions: {
    add(banner: Banner) {
      this.banners = [...this.banners, banner];
      this.counter = this.counter + 1;
    },
    addError(message: string, code: number = null): void {
      let err: Banner = { id: this.counter, message: message, type: BannerType.Error };

      if (code) {
        err.code = code;
        err = handleErrorCode(err);
      }

      this.add(err);
    },
    remove(id): void {
      this.banners = this.banners.filter((error) => error.id !== id);
    },
    _addBanner(banner: BannerResponse): void {
      let b: Banner = { id: this.counter, message: banner.message, type: banner.type };
      this.add(b);
    },
    handleBanners(res) {
      if (res.error?.value) {
        this.addError("Something went wrong! Please try again later.", 500);
      } else if (res.data.value?.error) {
        const error = res.data.value.error;
        this.addError(error.message, error.code);
      } else if (res.data.value.body.banner) {
        this._addBanner(res.data.value.body.banner);
      }
    },
  },
  persist: true,
});
