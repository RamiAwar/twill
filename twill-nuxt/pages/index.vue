<script setup lang="ts">
import { LockClosedIcon } from '@heroicons/vue/20/solid/index.d'
import { LoginRedirect } from '@/models/auth';

import { useUserStore } from '@/stores/user';

const userStore = useUserStore();

// Get login redirect
const loginRedirect = async () => {
  const res = await useFetch<LoginRedirect>('/api/auth/login')
  return navigateTo(res.data.value.redirect_url, { external: true });
}

const logout = async () => {
  const res = await useFetch('/api/auth/logout')
  userStore.logout();
  return navigateTo("/");
}

console.log(userStore.isLoggedIn);

</script> 
  
<template>
  <div v-if="!userStore.isLoggedIn" class="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-md space-y-8">
      <div>
        <img class="mx-auto h-24 w-auto" src="/images/logo.png" alt="Your Company" />
        <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">Sign in to your account</h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Or
          {{ ' ' }}
          <a href="#" class="font-medium text-blue-600 hover:text-blue-500">start your 14-day free trial</a>
        </p>
      </div>
      <div>
        <button type="submit" @click="loginRedirect"
          class="group relative flex w-full justify-center rounded-md border border-transparent bg-blue-600 py-2 px-4 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">
          <span class="absolute inset-y-0 left-0 flex items-center pl-3">
            <LockClosedIcon class="h-5 w-5 text-blue-500 group-hover:text-blue-400" aria-hidden="true" />
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