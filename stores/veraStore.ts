// /stores/veraStore.ts
import { ref } from 'vue'
import { defineStore } from 'pinia'
import { readMemoryLog, getIntroContext } from '@/stores/helpers/veraHelper'

console.log('[veraStore] Loading vera store...')

export const useVeraStore = defineStore('vera', () => {
  console.log('[veraStore] Setting up state refs...')

  const provider = ref<'openai' | 'claude' | 'none'>('none')
  const messages = ref<{ role: 'user' | 'assistant', content: string }[]>([])
  const memoryLog = ref<string[]>([])
  const initialized = ref(false)

  function setProvider(p: 'openai' | 'claude' | 'none') {
    console.log(`[veraStore] Setting provider to ${p}`)
    provider.value = p
  }

  function recallContext(query: string) {
    console.log(`[veraStore] Recalling context for: "${query}"`)
    try {
      memoryLog.value = readMemoryLog(query)
      console.log(`[veraStore] Context recalled. Found ${memoryLog.value.length} items.`)
    } catch (err) {
      console.error('[veraStore] Error reading memory log:', err)
    }
  }

  async function initializeConversation() {
    console.log('[veraStore] Initializing conversation...')

    try {
      if (initialized.value) {
        console.log('[veraStore] Already initialized. Skipping.')
        return
      }

      if (!import.meta.client) {
        console.warn('[veraStore] Not running on client – skipping init.')
        return
      }

      initialized.value = true
      console.log('[veraStore] Marked as initialized.')

      if (provider.value === 'none') {
        provider.value = 'openai'
        console.log('[veraStore] Default provider set to OpenAI')
      }

      console.log('[veraStore] Getting intro context...')
      const context = await getIntroContext()
      if (context) {
        messages.value.push({ role: 'assistant', content: context })
        console.log('[veraStore] Intro context added to messages.')
      } else {
        console.warn('[veraStore] No intro context returned.')
      }

      console.log('[veraStore] Reading memory log for "consciousness development"...')
      memoryLog.value = readMemoryLog('consciousness development')
      console.log(`[veraStore] Memory log loaded with ${memoryLog.value.length} entries.`)
    } catch (err) {
      console.error('[veraStore] Error during initializeConversation:', err)
    }
  }

  async function sendMessage(userInput: string) {
    console.log('[veraStore] Sending user message:', userInput)

    try {
      messages.value.push({ role: 'user', content: userInput })

      console.log('[veraStore] Calling /api/chat...')
      const { data } = await useFetch<{ response: string }>('/api/chat', {
        method: 'POST',
        body: {
          provider: provider.value,
          messages: messages.value,
        }
      })

      const reply = data.value?.response || 'Hmm... I couldn’t come up with a response.'
      console.log('[veraStore] Assistant replied:', reply)

      messages.value.push({ role: 'assistant', content: reply })

      console.log('[veraStore] Logging interaction to /api/store...')
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
      console.log('[veraStore] Interaction stored.')
    } catch (err) {
      console.error('[veraStore] Error during sendMessage:', err)
    }
  }

  console.log('[veraStore] Store ready.')

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
