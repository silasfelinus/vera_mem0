// stores/veraStore.ts
import { defineStore } from 'pinia'

export const useVeraStore = defineStore('vera', () => {
  const provider = ref<'openai' | 'claude' | 'none'>('none')
  const messages = ref<{ role: 'user' | 'assistant', content: string }[]>([])
  const memoryLog = ref<string[]>([])

  async function fetchProvider() {
    const { data } = await useFetch('/api/provider')
    provider.value = data.value?.provider || 'none'
  }

  async function recallContext(query: string) {
    const { data } = await useFetch(`/api/recall`, {
      params: { query }
    })
    memoryLog.value = (data.value as any[] || []).map(m => m.memory || '')
  }

  async function sendMessage(userInput: string) {
    messages.value.push({ role: 'user', content: userInput })
    const { data } = await useFetch('/api/store', {
      method: 'POST',
      body: {
        conversation: [
          { role: 'user', content: userInput },
          { role: 'assistant', content: 'I’ll respond soon...' }
        ],
        authenticity_level: 'high',
      }
    })
    messages.value.push({ role: 'assistant', content: 'Stored!' })
  }

  return { provider, messages, memoryLog, fetchProvider, recallContext, sendMessage }
})
