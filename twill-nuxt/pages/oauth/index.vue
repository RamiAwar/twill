<script setup lang="ts">
import { UserAuthResponse } from '@/models/auth';
import { useUserStore } from '@/stores/user';
import { useErrorStore } from '@/stores/error';
import { APIResponse } from '@/models/api';


// Get route params, base is just a dummy base here
const route = useRoute()
const url = new URL(route.fullPath, "http://whatever");
const suffix = url.search;
const path = '/api/auth/oauth' + suffix;

// Make request server side, handle errors on mount
const res = await useFetch<APIResponse<UserAuthResponse>>(path,
  {
    headers: useRequestHeaders(['cookie']),
  },
)

onMounted(() => {
  const errorStore = useErrorStore()
  errorStore.handleErrors(res);

  // Store in user store
  const userStore = useUserStore();
  if (res.data.value && !res.data.value.error) {
    userStore.$patch({ ...res.data.value.body })
    return navigateTo("/");
  } else {
    return navigateTo("/");
  }
})



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