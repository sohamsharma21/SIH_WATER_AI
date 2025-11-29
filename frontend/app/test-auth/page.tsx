'use client'

import { useState } from 'react'
import { supabase } from '@/lib/supabase'

export default function TestAuthPage() {
  const [result, setResult] = useState<Record<string, any> | null>(null)
  const [email, setEmail] = useState('test@example.com')
  const [password, setPassword] = useState('test123456')

  const testSignup = async () => {
    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
      })
      setResult({ data, error, type: 'signup' })
    } catch (err: unknown) {
      setResult({ error: (err as Error)?.message ?? String(err), type: 'signup' })
    }
  }

  const testLogin = async () => {
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password,
      })
      setResult({ data, error, type: 'login' })
    } catch (err: unknown) {
      setResult({ error: (err as Error)?.message ?? String(err), type: 'login' })
    }
  }

  const testSession = async () => {
    try {
      const { data, error } = await supabase.auth.getSession()
      setResult({ data, error, type: 'session' })
    } catch (err: unknown) {
      setResult({ error: (err as Error)?.message ?? String(err), type: 'session' })
    }
  }

  return (
    <div className="min-h-screen p-8 bg-gray-100">
      <div className="max-w-2xl mx-auto bg-white p-6 rounded-lg shadow">
        <h1 className="text-2xl font-bold mb-4">Auth Test Page</h1>
        
        <div className="space-y-4 mb-6">
          <div>
            <label className="block mb-2">Email:</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <div>
            <label className="block mb-2">Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border rounded"
            />
          </div>
        </div>

        <div className="space-x-2 mb-6">
          <button
            onClick={testSignup}
            className="bg-blue-500 text-white px-4 py-2 rounded"
          >
            Test Signup
          </button>
          <button
            onClick={testLogin}
            className="bg-green-500 text-white px-4 py-2 rounded"
          >
            Test Login
          </button>
          <button
            onClick={testSession}
            className="bg-purple-500 text-white px-4 py-2 rounded"
          >
            Check Session
          </button>
        </div>

        {result && (
          <div className="mt-6 p-4 bg-gray-50 rounded">
            <h3 className="font-bold mb-2">Result ({result.type}):</h3>
            <pre className="text-xs overflow-auto">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}

        <div className="mt-6 p-4 bg-yellow-50 rounded">
          <h3 className="font-bold mb-2">Supabase Config:</h3>
          <p className="text-sm">
            URL: {process.env.NEXT_PUBLIC_SUPABASE_URL ? '✅ Set' : '❌ Missing'}<br />
            Key: {process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY ? '✅ Set' : '❌ Missing'}
          </p>
        </div>
      </div>
    </div>
  )
}

