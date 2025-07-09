<template>
  <div>
    <NuxtPage />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useVeraStore } from '@/stores/veraStore'

console.log('starting store')
const veraStore = useVeraStore()
console.log('called store')

onMounted(() => {
  console.log('starting initialization')
  veraStore.initializeConversation()
  console.log('finished initialization')
})
</script>
