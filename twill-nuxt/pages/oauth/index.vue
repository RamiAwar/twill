<script setup lang="ts">
import { UserAuthResponse } from '@/models/auth';
import { useUserStore } from '@/stores/user';
import { useBannerStore } from '@/stores/banner';
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
  const bannerStore = useBannerStore()
  bannerStore.handleBanners(res);

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
  <div class="flex items-center justify-center w-full h-full">
    <span class="flex justify-center items-center">
      <span class="animate-ping absolute inline-flex h-14 w-14 rounded-full bg-sky-400 opacity-75"></span>
      <span class="relative inline-flex rounded-full h-12 w-12 bg-gradient-to-b from-cyan-400 to-blue-400">
      </span>
    </span>
  </div>

</template>