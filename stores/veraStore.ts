// /stores/veraStore.ts
import { ref, onMounted } from 'vue'
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
    if (initialized.value) return
    initialized.value = true

    // Load local context and add as system message
    const context = await getIntroContext()
    if (context) {
      messages.value.push({ role: 'assistant', content: context })
    }
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

  onMounted(() => initializeConversation())

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

export type VeraStore = ReturnType<typeof useVeraStore>
