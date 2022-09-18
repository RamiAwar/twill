import { defineNuxtConfig } from "nuxt/config";

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  alias: {
    "class-validator": "class-validator/cjs/index.js",
  },
  buildModules: ["@nuxtjs/tailwindcss"],
  modules: ["@pinia/nuxt"],
  plugins: ["~/plugins/persistedstate.ts"],
  runtimeConfig: {
    API_URL: process.env.API_URL,
  },
});
