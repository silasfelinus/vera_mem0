<template>
  <div class="flex items-center gap-4">
    <span>Provider:</span>

    <span v-if="store.provider" class="font-bold">
      {{ store.provider }}
    </span>
    <span v-else class="text-gray-500 italic"> (loading...) </span>

    <button class="btn btn-sm" @click="store.fetchProvider()">🔄 Refresh</button>
  </div>
</template>

<script setup lang="ts">
import { useVeraStore } from '@/stores/veraStore'


const store = useVeraStore()

// Only fetch on client to avoid SSR errors
if (import.meta.client) {
  onMounted(() => store.fetchProvider())
}
</script>
