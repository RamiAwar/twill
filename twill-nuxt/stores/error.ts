import { defineStore } from "pinia";
import { ClientError } from "@/models/error";

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
      const err: ClientError = { id: this.counter, message: message };

      if (code) {
        err.code = code;
      }

      this.errors = [...this.errors, err];
      this.counter += 1;
    },
    remove(id): void {
      this.errors = this.errors.filter((error) => error.id !== id);
    },
  },
});
