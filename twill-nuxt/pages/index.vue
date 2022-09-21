<script setup lang="ts">
import { LockClosedIcon } from '@heroicons/vue/20/solid/index.js'
import { LoginRedirect } from '@/models/auth';
import { useUserStore } from '@/stores/user';
import { useErrorStore } from '@/stores/error';

const errorStore = useErrorStore()
const userStore = useUserStore();

// Get login redirect
const loginRedirect = async () => {
  const res = await useFetch('/api/auth/login');
  errorStore.handleErrors(res)
  return navigateTo(res.data.value.body.redirect_url, { external: true });
}

const logout = async () => {
  const res = await useFetch('/api/auth/logout');
  errorStore.handleErrors(res);
  userStore.logout();
  return navigateTo("/");
}
</script> 
  
<template>
  <div v-if="!userStore.isLoggedIn" class="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-md space-y-8 flex flex-col justify-center items-center">
      <div>
        <img class="mx-auto h-24 w-auto" src="/images/logo.png" alt="Your Company" />
        <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">Welcome to Twill!</h2>
        <!-- TODO: Add back in for trials? -->
        <!-- <p class="mt-2 text-center text-sm text-gray-600">
          Or
          {{ ' ' }}
          <a href="#" class="font-medium text-sky-600 hover:text-sky-500">start your 14-day free trial</a>
        </p> -->
      </div>
      <div class="w-3/4">
        <button type="submit" @click="loginRedirect"
          class="group relative flex w-full justify-center rounded-md border border-transparent bg-sky-500 py-2 px-4 text-sm font-medium text-white hover:bg-sky-600 focus:outline-none focus:ring-2 focus:ring-sky-400 focus:ring-offset-2">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3">
            <LockClosedIcon class="h-5 w-5 text-sky-300 group-hover:text-sky-400" aria-hidden="true" />
          </span>
          Sign in with Twitter
        </button>
      </div>
    </div>
  </div>
  <div v-else>
    Logged In
    <button @click="logout">Logout</button>
  </div>
</template>