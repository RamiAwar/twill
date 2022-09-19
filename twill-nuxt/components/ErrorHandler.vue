<script setup lang="ts">
import { useErrorStore } from '@/stores/error'
import { storeToRefs } from 'pinia'

// Subscribe to error store and display errors
const errorStore = useErrorStore()
const { errors } = storeToRefs(errorStore)

</script>

<template>
  <div class="absolute top-0 w-full">
    <ErrorBanner v-for="error in errors" v-bind="error" @close="errorStore.remove(error.id)" :key="error.id">
    </ErrorBanner>
  </div>
</template>