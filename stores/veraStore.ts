// /stores/veraStore.ts
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { readMemoryLog, getIntroContext } from '@/stores/helpers/veraHelper'

export const useVeraStore = defineStore('vera', () => {
  const provider = ref<'openai' | 'claude' | 'none'>('none')
  const messages = ref<{ role: 'user' | 'assistant', content: string }[]>([])
  const memoryLog = ref<string[]>([])
  const initialized = ref(false)

  function setProvider(p: 'openai' | 'claude' | 'none') {
    provider.value = p
  }

  function recallContext(query: string) {
    memoryLog.value = readMemoryLog(query)
  }

async function initializeConversation() {
  if (initialized.value || !import.meta.client) return
  initialized.value = true

  // Default provider
  if (provider.value === 'none') {
    provider.value = 'openai'
  }

  // Load intro context
  const context = await getIntroContext()
  if (context) {
    messages.value.push({ role: 'assistant', content: context })
  }

  // Load memory log automatically
  memoryLog.value = readMemoryLog('consciousness development')
}



  async function sendMessage(userInput: string) {
    messages.value.push({ role: 'user', content: userInput })

    const { data } = await useFetch<{ response: string }>('/api/chat', {
      method: 'POST',
      body: {
        provider: provider.value,
        messages: messages.value,
      }
    })

    const reply = data.value?.response || 'Hmm... I couldn’t come up with a response.'
    messages.value.push({ role: 'assistant', content: reply })

    await useFetch('/api/store', {
      method: 'POST',
      body: {
        conversation: [
          { role: 'user', content: userInput },
          { role: 'assistant', content: reply }
        ],
        authenticity_level: 'high',
      }
    })
  }



  return {
    provider,
    messages,
    memoryLog,
    setProvider,
    recallContext,
    sendMessage,
    initializeConversation
  }
})

