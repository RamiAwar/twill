<script setup lang="ts">
import { UserAuthResponse } from '@/models/auth';
import { useUserStore } from '@/stores/user';

// Get route params, base is just a dummy base here
const route = useRoute()
const url = new URL(route.fullPath, "http://whatever");
const suffix = url.search;

const res = await useFetch<UserAuthResponse>('/api/auth/oauth' + suffix,
  {
    headers: useRequestHeaders(['cookie'])
  }
);

// Store in user store
const userStore = useUserStore();
console.log(res.data.value);
if (res.data.value) {
  console.log("storing value in local storage", res.data.value)
  userStore.$patch({ ...res.data.value })
  navigateTo("/")
} else {
  // TODO: Push error here and clear cookies
  navigateTo("/");
}



</script>

<template>
  <div class="min-h-full bg-white px-4 py-16 sm:px-6 sm:py-24 md:grid md:place-items-center lg:px-8 flex items-center">
    <div class="mx-auto mh-auto max-w-max">
      <main class="sm:flex text-center">
        Loading...
      </main>
    </div>
  </div>
</template>