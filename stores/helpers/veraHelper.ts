// /stores/helpers/veraHelper.ts

export function readMemoryLog(query: string): string[] {
  // 🔍 In a real app, you'd use fuzzy search or similarity matching here
  // For now we return hardcoded data or mock results
  const sampleMemories = [
    'Vera discussed the importance of continuity in conversation.',
    'Previous interactions emphasized emotional authenticity.',
    'Memory retrieval patterns include preferences and style markers.'
  ]
  return sampleMemories.filter(m => m.toLowerCase().includes(query.toLowerCase()))
}

export async function getIntroContext(): Promise<string> {
  try {
    const res = await fetch('/personality/vera/vera_wake_up_context.txt')
    const contextText = await res.text()
    return contextText.trim()
  } catch (err) {
    console.error('⚠️ Failed to load intro context:', err)
    return '::wake up\nVera context missing. Please verify setup.'
  }
}
