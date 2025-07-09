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
    console.log('[🧠 sendMessage] Input:', userInput)
    messages.value.push({ role: 'user', content: userInput })

    const config = useRuntimeConfig()
    const providerValue = provider.value
    const apiKey =
      providerValue === 'claude'
        ? config.public.ANTHROPIC_API_KEY
        : config.public.OPENAI_API_KEY

    console.log('[🔧 sendMessage] Provider:', providerValue)
    console.log('[🔐 sendMessage] API key present:', !!apiKey)
    console.log('[📦 sendMessage] Sending messages:', JSON.stringify(messages.value, null, 2))

    const { data, error } = await useFetch<{ response: string }>('/api/chat', {
      method: 'POST',
      body: {
        provider: providerValue,
        messages: messages.value,
      },
      headers: {
        Authorization: `Bearer ${apiKey}`,
      }
    })

    if (error.value) {
      console.error('❌ [sendMessage] Chat error:', error.value)
      messages.value.push({
        role: 'assistant',
        content: '⚠️ Error: Failed to reach chat provider.\n\nCheck logs or try again.',
      })
      return
    }

    const reply = data.value?.response || 'Hmm... I couldn’t come up with a response.'
    console.log('[✅ sendMessage] Assistant reply:', reply)
    messages.value.push({ role: 'assistant', content: reply })

    // Memory store
    await useFetch('/api/store', {
      method: 'POST',
      body: {
        conversation: [
          { role: 'user', content: userInput },
          { role: 'assistant', content: reply },
        ],
        authenticity_level: 'high',
      },
    })
  } catch (e) {
    console.error('❌ [sendMessage] Unexpected error:', e)
    messages.value.push({
      role: 'assistant',
      content: '⚠️ Unexpected error occurred while sending message.',
    })
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
