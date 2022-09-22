<script setup lang="ts">
import { LockClosedIcon } from '@heroicons/vue/20/solid/index.js'
import { useBannerStore } from '@/stores/banner';

const bannerStore = useBannerStore()

const email = ref("");

const betaSignup = async () => {
  console.log("sending")
  const res = await useFetch('/api/beta/signup', {
    method: "POST",
    body: {
      email: email.value
    }
  });
  bannerStore.handleBanners(res)
  return navigateTo("/");
}
</script>

<template>
  <div class="flex min-h-full items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="w-full max-w-sm space-y-8">
      <div>
        <img class="mx-auto h-24 w-auto" src="/images/logo.png" alt="Twill" />
        <h2 class="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">Sign up for beta waitlist</h2>
      </div>
      <div class="mt-8 space-y-6">
        <input type="hidden" name="remember" value="true" />
        <div class="-space-y-px rounded-md shadow-sm">
          <div>
            <label for="email-address" class="sr-only">Email address</label>
            <input id="email-address" v-model="email" name="email" type="email" autocomplete="email" required="true"
              class="relative block w-full appearance-none rounded-md border border-gray-300 px-3 py-2 text-gray-900 placeholder-gray-500 focus:z-10 focus:border-blue-400 focus:outline-none focus:ring-blue-400 sm:text-sm"
              placeholder="Email address" />
          </div>
        </div>

        <div>
          <button @click="betaSignup"
            class="group relative flex w-full justify-center rounded-md border border-transparent bg-blue-500 py-2 px-4 text-sm font-medium text-white hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2">
            <span class="absolute inset-y-0 left-0 flex items-center pl-3">
              <LockClosedIcon class="h-5 w-5 text-blue-400 group-hover:text-blue-500" aria-hidden="true" />
            </span>
            Sign in
          </button>
        </div>
      </div>
    </div>
  </div>
</template>