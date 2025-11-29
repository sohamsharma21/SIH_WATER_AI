"use client"

import { useEffect, useState, useRef } from 'react'
import { supabase } from '@/lib/supabase'
import { api } from '@/lib/api'
import type { PlantStatus } from '@/lib/types'

export default function useTwinRealtime(initial?: PlantStatus | null) {
  const [twinState, setTwinState] = useState<PlantStatus | null>(initial ?? null)
  const mounted = useRef(true)

  // fetch latest snapshot
  async function refresh() {
    try {
      const res = await api.getTwinStatus()
      if (!mounted.current) return
      if (res?.data) setTwinState(res.data as PlantStatus)
    } catch (err) {
      // swallow — component will still show last known state
      console.warn('useTwinRealtime: failed to refresh twin status', err)
    }
  }

  useEffect(() => {
    mounted.current = true
    // initial up-to-date snapshot
    refresh()

    // subscribe to sensors and predictions insert events — reload snapshot on changes
    let sensorsChannel: any = null
    let predictionsChannel: any = null

    try {
      sensorsChannel = supabase
        .channel('twin-sensors')
        .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'sensors' }, () => {
          refresh()
        })
        .subscribe()

      predictionsChannel = supabase
        .channel('twin-predictions')
        .on('postgres_changes', { event: 'INSERT', schema: 'public', table: 'predictions' }, () => {
          refresh()
        })
        .subscribe()
    } catch (e) {
      console.warn('useTwinRealtime: realtime subscription failed', e)
    }

    return () => {
      mounted.current = false
      if (sensorsChannel) sensorsChannel.unsubscribe()
      if (predictionsChannel) predictionsChannel.unsubscribe()
    }
  }, [])

  // accept outside updates (for example Dashboard prop updates)
  useEffect(() => {
    if (initial) setTwinState(initial)
  }, [initial])

  return { twinState, refresh }
}
