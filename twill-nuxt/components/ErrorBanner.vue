<script setup lang="ts">
import { ExclamationCircleIcon, XMarkIcon } from '@heroicons/vue/24/outline/index.js'

interface ErrorProps {
  // Error
  message: string;
  id: number;
  code?: number;

  // Banner properties
  dismissable?: boolean;
  ephemeral?: boolean;
  timeout?: number;
}

const props = withDefaults(defineProps<ErrorProps>(), {
  dismissable: true,
  ephemeral: true,
  timeout: 5000,
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
      <div class="sm:rounded-lg bg-red-500 p-2 shadow-lg sm:p-3">
        <div class="flex flex-wrap items-center justify-between">
          <div class="flex w-0 flex-1 items-center">
            <span class="flex rounded-lg bg-red-700 p-2">
              <ExclamationCircleIcon class="h-6 w-6 text-white" aria-hidden="true" />
            </span>
            <p class="ml-3 truncate font-medium text-white">
              <span class="md:inline">{{ message }}</span>
            </p>
          </div>
          <div class="order-2 flex-shrink-0 sm:order-3 sm:ml-2">
            <button type="button" @click="dismiss"
              class="-mr-1 flex rounded-md p-2 hover:bg-red-400 focus:outline-none focus:ring-2 focus:ring-white">
              <span class="sr-only">Dismiss</span>
              <XMarkIcon class="h-6 w-6 text-white" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
