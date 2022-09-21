import { defineStore } from "pinia";
import { ClientError } from "@/models/error";
import routes from "@/routes";

function handleErrorCode(error: ClientError) {
  switch (error.code) {
    case 412:
      error.meta = "Signup for beta";
      error.link = routes.beta_signup;
      return error;
  }
}

export const useErrorStore = defineStore("error", {
  state() {
    return {
      counter: 0,
      errors: [] as ClientError[],
    };
  },
  getters: {},
  actions: {
    add(message: string, code: number = null): void {
      let err: ClientError = { id: this.counter, message: message };

      if (code) {
        err.code = code;
        err = handleErrorCode(err);
      }

      this.errors = [...this.errors, err];
      this.counter = this.counter + 1;
    },
    remove(id): void {
      this.errors = this.errors.filter((error) => error.id !== id);
    },
    handleErrors(res) {
      if (res.error?.value) {
        this.add("Something went wrong! Please try again later.", 500);
      } else if (res.data.value?.error) {
        const error = res.data.value.error;
        this.add(error.message, error.code);
      }
    },
  },
  persist: true,
});
