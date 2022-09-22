<script setup lang="ts">
import { ExclamationCircleIcon, XMarkIcon, InformationCircleIcon } from '@heroicons/vue/24/outline/index.js'


interface BannerProps {
  // Error
  message: string;
  id: number;
  code?: number;

  // Banner properties
  dismissable?: boolean;
  ephemeral?: boolean;
  timeout?: number;
  meta?: string;
  link?: string;
}

const props = withDefaults(defineProps<BannerProps>(), {
  dismissable: true,
  ephemeral: true,
  timeout: 9000,
})

const emit = defineEmits(['close'])
function dismiss() {
  emit('close')
}

// Auto dismiss after timeout if ephemeral is set
onMounted(() => {
  if (props.ephemeral) {
    setTimeout(() => {
      dismiss()
    }, props.timeout)
  }
})

</script>
    
<template>
  <div class="inset-x-0 mt-2">
    <div class="sm:mx-auto max-w-7xl sm:px-2 md:px-6 lg:px-8">
      <div class="sm:rounded-lg bg-blue-500 p-2 shadow-lg sm:p-3">
        <div class="flex flex-wrap items-center justify-between">
          <div class="flex w-0 flex-1 items-center">
            <span class="flex rounded-lg bg-blue-700 p-2">
              <InformationCircleIcon class="h-6 w-6 text-white" aria-hidden="true" />
            </span>
            <p class="ml-3 truncate font-medium text-white">
              <span class="md:inline">{{ message }}</span>
            </p>
          </div>
          <div v-if="meta" class="order-3 mt-2 w-full flex-shrink-0 sm:order-2 sm:mt-0 sm:w-auto">
            <a :href="link" @click="dismiss"
              class="flex items-center justify-center rounded-md border border-transparent bg-white px-4 py-2 text-sm font-medium text-blue-600 shadow-sm hover:bg-blue-50">{{
              meta }}</a>
          </div>
          <div class="order-2 flex-shrink-0 sm:order-3 sm:ml-2">
            <button type="button" @click="dismiss"
              class="-mr-1 flex rounded-md p-2 hover:bg-blue-400 focus:outline-none focus:ring-2 focus:ring-white">
              <span class="sr-only">Dismiss</span>
              <XMarkIcon class="h-6 w-6 text-white" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
    