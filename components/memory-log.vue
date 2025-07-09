<!-- /components/vera-memory-log.vue -->
<template>
  <div class="mt-6 bg-base-100 rounded-md shadow p-4 border border-base-300">
    <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
      🧠 <span>Memory Log</span>
    </h3>

    <ul class="space-y-2 text-sm text-base-content max-h-64 overflow-y-auto pr-2">
      <li
        v-for="(m, i) in memoryLog"
        :key="i"
        class="flex items-start gap-2 bg-base-200 rounded p-2"
      >
        <span class="text-primary mt-0.5">🧠</span>
        <span class="whitespace-pre-line leading-snug">{{ m }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useVeraStore } from '@/stores/veraStore'

const veraStore = useVeraStore()
const memoryLog = computed(() => veraStore?.memoryLog ?? [])
</script>
