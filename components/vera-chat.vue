<!-- /components/vera-chat.vue -->
<template>
  <div class="bg-base-100 mx-auto max-w-2xl space-y-4 rounded-lg p-4 shadow-lg">
    <!-- Chat Display -->
    <div class="space-y-3">
      <div
        v-for="(m, i) in messages"
        :key="i"
        :class="[
          'rounded-md p-3',
          m.role === 'user' ? 'bg-primary/10 text-primary' : 'bg-accent/10 text-accent',
        ]"
      >
        <span class="mb-1 block text-sm font-semibold tracking-wide uppercase">
          {{ m.role }}
        </span>
        <p class="text-sm leading-relaxed whitespace-pre-line">
          {{ m.content }}
        </p>
      </div>
    </div>

    <!-- Chat Input -->
    <form class="flex items-center gap-2" @submit.prevent="send">
      <input
        v-model="input"
        type="text"
        placeholder="Type your message..."
        class="input input-bordered w-full"
      />
      <button type="submit" class="btn btn-primary">Send</button>
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
