import { defineNuxtConfig } from "nuxt/config";

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  modules: ["@pinia/nuxt", "@nuxtjs/tailwindcss"],
  plugins: ["~/plugins/persistedstate.ts"],
  runtimeConfig: {
    API_URL: process.env.API_URL,
  },
});
