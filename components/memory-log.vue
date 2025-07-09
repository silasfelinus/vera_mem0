<template>
  <div class="mt-4">
    <h3 class="font-bold mb-2">Memory Log</h3>
    <ul class="space-y-1">
      <li v-for="(m, i) in store.memoryLog" :key="i">🧠 {{ m }}</li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useVeraStore } from '@/stores/veraStore'


const store = useVeraStore()
onMounted(() => store.recallContext('consciousness development'))
</script>
