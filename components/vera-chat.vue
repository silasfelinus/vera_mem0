<!-- /components/vera-chat.vue -->
<template>
  <div>
    <div class="space-y-2 mb-4">
      <div v-for="(m, i) in messages" :key="i" :class="m.role">
        <span class="font-bold">{{ m.role }}:</span> {{ m.content }}
      </div>
    </div>

    <form @submit.prevent="send">
      <input
        v-model="input"
        placeholder="Type something..."
        class="input input-bordered w-full"
      />
    </form>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useVeraStore } from '@/stores/veraStore'

const veraStore = useVeraStore()

const messages = computed(() => veraStore?.messages ?? [])

const input = ref('')

function send() {
  if (!veraStore) return
  const text = input.value.trim()
  if (text) {
    veraStore.sendMessage(text)
    input.value = ''
  }
}
</script>

<style scoped>
.user {
  color: #4b5563;
}
.assistant {
  color: #2563eb;
}
</style>
