<template>
  <div class="flex items-center gap-4">
    <span>Provider:</span>

    <span v-if="store.provider !== 'none'" class="font-bold">
      {{ store.provider }}
    </span>
    <span v-else class="text-gray-500 italic"> (not set) </span>

    <button class="btn btn-sm" @click="cycleProvider">🔄 Switch</button>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useVeraStore } from '@/stores/veraStore'

const store = useVeraStore()

function cycleProvider() {
  const next = {
    none: 'openai',
    openai: 'claude',
    claude: 'none',
  }[store.provider] as 'openai' | 'claude' | 'none'

  store.setProvider(next)
}

onMounted(() => {
  // Default to OpenAI if none set
  if (store.provider === 'none') {
    store.setProvider('openai')
  }
})
</script>
