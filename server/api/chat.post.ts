// /server/api/chat.post.ts
import { defineEventHandler, readBody, createError } from 'h3'
import OpenAI from 'openai'
import { Anthropic } from '@anthropic-ai/sdk'

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const provider: 'openai' | 'claude' = body.provider
  const messages = body.messages

  if (!provider || !messages) {
    throw createError({ statusCode: 400, message: 'Missing provider or messages' })
  }

  try {
    if (provider === 'openai') {
      const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })
      const response = await openai.chat.completions.create({
        model: 'gpt-4-turbo',
        messages,
        temperature: 0.7
      })
      return { response: response.choices[0].message.content }
    }

    if (provider === 'claude') {
      const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })
      const response = await anthropic.messages.create({
        model: 'claude-3-opus-20240229',
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
    console.error('❌ Chat error:', err)
    throw createError({ statusCode: 500, message: (err as Error).message || 'Unknown error' })
  }
})