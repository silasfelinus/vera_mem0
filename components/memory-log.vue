<template>
  <div class="mt-4">
    <h3 class="mb-2 font-bold">Memory Log</h3>
    <ul class="space-y-1">
      <li v-for="(m, i) in memoryLog" :key="i">🧠 {{ m }}</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useVeraStore } from '@/stores/veraStore'
import type { VeraStore } from '@/stores/veraStore'

const veraStore = import.meta.client ? useVeraStore() : (null as VeraStore | null)

const memoryLog = computed(() => veraStore?.memoryLog ?? [])

onMounted(() => veraStore?.recallContext('consciousness development'))
</script>
