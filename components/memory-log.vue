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

const veraStore = useVeraStore()

const memoryLog = computed(() => veraStore?.memoryLog ?? [])


</script>
