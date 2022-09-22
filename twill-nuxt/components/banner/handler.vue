<script setup lang="ts">
import { useBannerStore } from '@/stores/banner'

import { storeToRefs } from 'pinia'

// This code needs to be duplicated as vue3 components are compiled in isolation
enum BannerType {
  Error = 'error',
  Warning = 'warning',
  Info = 'info',
  Success = 'success',
}

// Subscribe to error store and display errors
const bannerStore = useBannerStore()
const { banners } = storeToRefs(bannerStore)


const BannerError = resolveComponent("BannerError")
const BannerInfo = resolveComponent("BannerInfo")
const BannerSuccess = resolveComponent("BannerSuccess")

function getBanner(type: BannerType) {
  switch (type) {
    case BannerType.Error:
      return BannerError
    case BannerType.Info:
      return BannerInfo
    case BannerType.Success:
      return BannerSuccess
    default:
      return BannerError
  }
}

</script>

<template>
  <div class="absolute top-0 w-full">
    <component v-for="banner in banners" v-bind:is="getBanner(banner.type)" v-bind="banner"
      @close="bannerStore.remove(banner.id)" :key="banner.id">
    </component>
  </div>
</template>