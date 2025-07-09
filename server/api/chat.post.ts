// /server/api/chat.post.ts
import { defineEventHandler, readBody, createError } from 'h3'
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

  try {
    if (provider === 'openai') {
      console.log('🤖 [chat.post] Using OpenAI...')
      const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
      const response = await openai.chat.completions.create({
        model: 'gpt-4-turbo',
        messages,
        temperature: 0.7
      })
      console.log('✅ [chat.post] OpenAI response received')
      return { response: response.choices[0].message.content }
    }

    if (provider === 'claude') {
      console.log('🧠 [chat.post] Using Claude...')
      const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })
      const response = await anthropic.messages.create({
        model: 'claude-3-opus-20240229',
        messages,
        max_tokens: 1024,
        temperature: 0.7
      })

      console.log('✅ [chat.post] Claude raw response:', JSON.stringify(response, null, 2))

      const content = response.content?.find(c => 'text' in c)
      if (!content || typeof content.text !== 'string') {
        console.error('❌ [chat.post] Claude response had unexpected format:', response.content)
        throw new Error('Claude returned unexpected content format')
      }

      return { response: content.text }
    }

    console.error('❌ [chat.post] Unsupported provider:', provider)
    throw createError({ statusCode: 400, message: 'Unsupported provider' })
  } catch (err: unknown) {
    console.error('❌ [chat.post] Chat error:', err)
    throw createError({
      statusCode: 500,
      message: (err as Error).message || 'Unknown server error'
    })
  }
})
