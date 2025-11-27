'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '@/lib/supabase'
import Dashboard from '@/components/Dashboard'

export default function DashboardPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    checkAuth()
    
    // Listen for auth state changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {
      if (event === 'SIGNED_OUT' || !session) {
        router.push('/login')
      } else if (event === 'SIGNED_IN') {
        setLoading(false)
      }
    })

    return () => {
      subscription.unsubscribe()
    }
  }, [router])

  const checkAuth = async () => {
    try {
      const { data: { session }, error } = await supabase.auth.getSession()
      if (error) {
        console.error('Auth error:', error)
        router.push('/login')
        return
      }
      if (!session) {
        router.push('/login')
      } else {
        setLoading(false)
      }
    } catch (err) {
      console.error('Auth check error:', err)
      router.push('/login')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold text-blue-700">SIH WATER AI</h1>
          <div className="space-x-4">
            <a href="/dashboard" className="text-gray-700 hover:text-blue-600">
              Dashboard
            </a>
            <a href="/reports" className="text-gray-700 hover:text-blue-600">
              Reports
            </a>
            <a href="/admin" className="text-gray-700 hover:text-blue-600">
              Admin
            </a>
            <button
              onClick={async () => {
                await supabase.auth.signOut()
                router.push('/login')
              }}
              className="text-red-600 hover:text-red-800"
            >
              Logout
            </button>
          </div>
        </div>
      </nav>
      <Dashboard />
    </div>
  )
}

