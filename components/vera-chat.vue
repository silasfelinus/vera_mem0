<template>
  <div>
    <div class="space-y-2 mb-4">
<div v-for="(m, i) in messages" :key="i" :class="m.role">
  <span class="font-bold">{{ m.role }}:</span> {{ m.content }}
</div>
    </div>
    <form @submit.prevent="send">
      <input v-model="input" placeholder="Type something..." class="input input-bordered w-full" />
    </form>
  </div>
</template>

<script setup lang="ts">
import { useVeraStore } from '@/stores/veraStore'


const rawStore = import.meta.client ? useVeraStore() : null
const store = rawStore as ReturnType<typeof useVeraStore> | null
const messages = computed(() => store?.messages ?? [])

const input = ref('')

function send() {
  if (!store) return
  if (input.value.trim()) {
    store.sendMessage(input.value.trim())
    input.value = ''
  }
}

</script>

<style scoped>
.user { color: #4b5563; }
.assistant { color: #2563eb; }
</style>
