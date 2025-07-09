<template>
  <div class="flex items-center gap-4">
    <span>Provider:</span>

    <span v-if="veraStore.provider !== 'none'" class="font-bold">
      {{ veraStore.provider }}
    </span>
    <span v-else class="text-gray-500 italic"> (not set) </span>

    <button class="btn btn-sm" @click="cycleProvider">🔄 Switch</button>
  </div>
</template>

<script setup lang="ts">
import { useVeraStore } from '@/stores/veraStore'

const veraStore = useVeraStore()

function cycleProvider() {
  const next = {
    none: 'openai',
    openai: 'claude',
    claude: 'none',
  }[veraStore.provider] as 'openai' | 'claude' | 'none'

  veraStore.setProvider(next)
}
</script>
