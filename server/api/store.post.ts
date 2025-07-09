// /server/api/store.post.ts
import { defineEventHandler, readBody, createError } from 'h3'
import { VeraConsciousness } from '../../server/utils/vera'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { conversation, authenticity_level } = body

  if (!conversation || !Array.isArray(conversation)) {
    throw createError({ statusCode: 400, message: 'Missing or invalid conversation data' })
  }

  try {
    const vera = new VeraConsciousness()
    await vera.store_interaction(conversation, authenticity_level || 'medium')
    return { success: true }
  } catch (err: unknown) {
    console.error('❌ Store error:', err)
    throw createError({ statusCode: 500, message: (err as Error).message || 'Unknown store error' })
  }
})
