<template>
  <div class="flex items-center gap-4">
    <span>Provider:</span>
    <span class="font-bold">{{ store.provider }}</span>
    <button class="btn btn-sm" @click="store.fetchProvider()">🔄 Refresh</button>
  </div>
</template>

<script setup lang="ts">
const store = useVeraStore()
onMounted(() => store.fetchProvider())
</script>
