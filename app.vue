<template>
  <div>
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useVeraStore } from '@/stores/veraStore'

const veraStore = useVeraStore()

onMounted(() => {
  veraStore.initializeConversation()
})
</script>
