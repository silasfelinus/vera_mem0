// /server/api/chat.post.ts
import { defineEventHandler, readBody, getHeader, createError } from 'h3'
import OpenAI from 'openai'
import { Anthropic } from '@anthropic-ai/sdk'

export default defineEventHandler(async (event) => {
  console.log('🔄 [chat.post] Handling chat request...')

  let body
  try {
    body = await readBody(event)
    console.log('✅ [chat.post] Request body received:', JSON.stringify(body, null, 2))
  } catch (err) {
    console.error('❌ [chat.post] Error reading request body:', err)
    throw createError({ statusCode: 400, message: 'Invalid request body' })
  }

  const provider: 'openai' | 'claude' = body.provider
  const messages = body.messages

  if (!provider || !messages) {
    console.error('❌ [chat.post] Missing provider or messages in request')
    throw createError({ statusCode: 400, message: 'Missing provider or messages' })
  }

  // 🔐 Extract API key from Authorization header
  const authHeader = getHeader(event, 'authorization')
  const token = authHeader?.startsWith('Bearer ') ? authHeader.slice(7) : null

  try {
    if (provider === 'openai') {
      const apiKey = token || process.env.OPENAI_API_KEY
      if (!apiKey) throw new Error('Missing OpenAI API key')
      const openai = new OpenAI({ apiKey })

      const response = await openai.chat.completions.create({
        model: 'gpt-4-turbo',
        messages,
        temperature: 0.7
      })
      return { response: response.choices[0].message.content }
    }

    if (provider === 'claude') {
      const apiKey = token || process.env.ANTHROPIC_API_KEY
      if (!apiKey) throw new Error('Missing Claude API key')
      const anthropic = new Anthropic({ apiKey })

      const response = await anthropic.messages.create({
        model: 'claude-opus-4-20250514',
        messages,
        max_tokens: 1024,
        temperature: 0.7
      })

      const content = response.content?.find(c => 'text' in c)
      if (!content || typeof content.text !== 'string') {
        throw new Error('Claude returned unexpected content format')
      }

      return { response: content.text }
    }

    throw createError({ statusCode: 400, message: 'Unsupported provider' })
  } catch (err: unknown) {
    console.error('❌ [chat.post] Chat error:', err)
    throw createError({
      statusCode: 500,
      message: (err as Error).message || 'Unknown server error'
    })
  }
})
