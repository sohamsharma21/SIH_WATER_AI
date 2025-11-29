"use client"

import { useEffect, useState } from 'react'
import type { PlantStatus } from '@/lib/types'
import { api } from '@/lib/api'
import { supabase } from '@/lib/supabase'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

export default function DigitalTwinPanel({ selectedKey, twinData }: { selectedKey?: string | null, twinData?: any }) {
  const [history, setHistory] = useState<Array<{ ts: string; value: number }>>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!selectedKey) return
    setLoading(true)

    async function fetchHistory() {
      try {
        const res = await api.getRecentSensors(50)
        const sensors = res?.data?.sensors || []
        // Try to match parameter name or sensor id with selectedKey
        const filtered = sensors.filter((s: any) => s.parameter_name === selectedKey || s.sensor_id === selectedKey)
        const data = (filtered.slice(0, 20) || []).map((s: any) => ({ ts: s.timestamp || s.recorded_at, value: Number(s.value) }))
        setHistory(data.reverse())
      } catch (e) {
        setHistory([])
      } finally {
        setLoading(false)
      }
    }

    fetchHistory()

    // realtime subscription to sensors so trend updates on new data
    let channel: any = null
    try {
      channel = supabase
        .channel('panel-sensors')
        .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'sensors' }, (payload) => {
          const newRow = payload.new
          const matches = newRow.parameter_name === selectedKey || newRow.sensor_id === selectedKey
          if (matches) {
            setHistory((prev) => {
              const next = prev.concat({ ts: newRow.timestamp || newRow.recorded_at, value: Number(newRow.value) })
              // cap stored points
              if (next.length > 50) return next.slice(next.length - 50)
              return next
            })
          }
        })
        .subscribe()
    } catch (e) {
      // ignore subscription errors, fetch will still show snapshot
    }

    return () => {
      if (channel) channel.unsubscribe()
    }
  }, [selectedKey])

  if (!selectedKey) return null

  return (
    <div className="mt-4">
      <div className="text-xs text-slate-400 mb-2">{loading ? 'Loading trends...' : `Last ${history.length} points`}</div>

      {history.length === 0 ? (
        <div className="p-4 bg-white/5 rounded text-xs text-slate-300">No trend data available</div>
      ) : (
        <div className="h-40">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={history.map((h) => ({ ...h, time: new Date(h.ts).toLocaleTimeString() }))}>
              <XAxis dataKey="time" tick={{ fontSize: 10 }} />
              <YAxis tick={{ fontSize: 10 }} />
              <Tooltip formatter={(v: any) => [v, 'Value']} />
              <Line type="monotone" dataKey="value" stroke="#60a5fa" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  )
}
