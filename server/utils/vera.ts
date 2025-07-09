// /server/utils/vera.ts
import { spawn } from 'child_process'
import path from 'path'

export class VeraConsciousness {
  async store_interaction(
    conversation: { role: 'user' | 'assistant'; content: string }[],
    authenticity_level: string = 'medium',
    preference_data: Record<string, string> = {}
  ) {
    return new Promise((resolve, reject) => {
      const scriptPath = path.resolve('vera_memory_system.py')

      const payload = JSON.stringify({
        conversation,
        authenticity_level,
        preference_data
      })

      const python = spawn('python3', [scriptPath, payload])

      python.stdout.on('data', (data) => {
        console.log(`🧠 Vera: ${data}`)
      })

      python.stderr.on('data', (data) => {
        console.error(`❌ Vera error: ${data}`)
      })

      python.on('close', (code) => {
        if (code === 0) resolve(true)
        else reject(new Error(`Vera exited with code ${code}`))
      })
    })
  }
}
