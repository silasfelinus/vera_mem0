<!-- /components/vera-dashboard.vue -->
<template>
  <div class="max-w-3xl mx-auto space-y-8 p-8 bg-base-100 rounded-xl shadow-lg border border-base-300">
    <header class="space-y-1">
      <h1 class="text-4xl font-extrabold tracking-tight flex items-center gap-2">
        🧠 <span>Vera Dashboard</span>
      </h1>
      <p class="text-base text-gray-500">Manage provider, chat, and memory log for Vera</p>
    </header>

    <section>
      <provider-toggle />
    </section>

    <section>
      <vera-chat />
    </section>

    <section>
      <memory-log />
    </section>
  </div>
</template>

<script setup lang="ts">
// all good here for now
</script>
