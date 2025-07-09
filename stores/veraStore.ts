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
    try {
      memoryLog.value = readMemoryLog(query)
    } catch {
      console.log("recall failed")
    }
  }

  async function initializeConversation() {
    if (initialized.value || !import.meta.client) return
    initialized.value = true
    if (provider.value === 'none') provider.value = 'openai'

    const context = await getIntroContext()
    if (context) {
      messages.value.push({ role: 'assistant', content: context })
    }

    memoryLog.value = readMemoryLog('consciousness development')
  }

   async function sendMessage(userInput: string) {
    try {
      messages.value.push({ role: 'user', content: userInput })

      const apiKey =
        provider.value === 'claude'
          ? import.meta.env.ANTHROPIC_API_KEY
          : import.meta.env.OPENAI_API_KEY

      const { data } = await useFetch<{ response: string }>('/api/chat', {
        method: 'POST',
        body: {
          provider: provider.value,
          messages: messages.value,
        },
        headers: {
          Authorization: `Bearer ${apiKey}`,
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
    } catch {
      console.log("send message failed")
    }
  }


  return {
    provider,
    messages,
    memoryLog,
    initialized,
    setProvider,
    recallContext,
    sendMessage,
    initializeConversation,
  }
})
