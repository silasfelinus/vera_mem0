<!-- /components/vera-provider-toggle.vue -->
<template>
  <div
    class="bg-base-100 border-base-300 flex items-center gap-3 rounded-md border px-4 py-2 shadow-sm"
  >
    <span class="text-base-content text-sm font-medium">Provider:</span>

    <span
      v-if="veraStore.provider !== 'none'"
      class="bg-primary/10 text-primary rounded px-2 py-1 text-sm font-semibold"
    >
      {{ veraStore.provider }}
    </span>
    <span v-else class="bg-base-200 rounded px-2 py-1 text-sm text-gray-500 italic"> not set </span>

    <button
      class="btn btn-sm btn-outline ml-auto"
      title="Cycle between OpenAI and Claude"
      @click="cycleProvider"
    >
      🔄 Switch
    </button>
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
