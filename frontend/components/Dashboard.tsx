'use client'

import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import { supabase } from '@/lib/supabase'
import DigitalTwin from './DigitalTwin'
import SensorDashboard from './SensorDashboard'
import PredictionCard from './PredictionCard'
import TreatmentOptimizer from './TreatmentOptimizer'
import PredictionForm from './PredictionForm'

export default function Dashboard() {
  const [twinStatus, setTwinStatus] = useState<any>(null)
  const [predictions, setPredictions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadDashboardData()
    const interval = setInterval(loadDashboardData, 10000) // Refresh every 10 seconds
    
    // Set up Supabase Realtime subscriptions - with error handling
    let sensorsChannel: any = null
    let predictionsChannel: any = null
    
    try {
      sensorsChannel = supabase
        .channel('sensors')
        .on('postgres_changes', 
          { event: 'INSERT', schema: 'public', table: 'sensors' },
          (payload) => {
            console.log('New sensor data:', payload.new)
            loadDashboardData() // Reload on new sensor data
          }
        )
        .subscribe()

      predictionsChannel = supabase
        .channel('predictions')
        .on('postgres_changes',
          { event: 'INSERT', schema: 'public', table: 'predictions' },
          (payload) => {
            console.log('New prediction:', payload.new)
            loadDashboardData() // Reload on new prediction
          }
        )
        .subscribe()
    } catch (subError) {
      console.warn('Error subscribing to realtime:', subError)
    }

    return () => {
      clearInterval(interval)
      if (sensorsChannel) sensorsChannel.unsubscribe()
      if (predictionsChannel) predictionsChannel.unsubscribe()
    }
  }, [])

  const loadDashboardData = async () => {
    try {
      setError(null)
      const [twinRes, predictionsRes] = await Promise.all([
        api.getTwinStatus().catch(err => {
          console.warn('Error fetching twin status:', err)
          return { data: { 
            status: 'error',
            sensor_status: {}, 
            latest_prediction: null, 
            twin_state: {} 
          } }
        }),
        api.getRecentPredictions(5).catch(err => {
          console.warn('Error fetching predictions:', err)
          return { data: { 
            status: 'error',
            predictions: [] 
          } }
        }),
      ])

      setTwinStatus(twinRes.data)
      setPredictions(predictionsRes.data.predictions || [])
      setLoading(false)
    } catch (error) {
      console.error('Error loading dashboard:', error)
      setError('Failed to load dashboard data')
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-xl">Loading dashboard...</div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Dashboard</h1>
      
      {error && (
        <div className="mb-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Digital Twin */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Digital Twin</h2>
          <DigitalTwin status={twinStatus} />
        </div>

        {/* Sensor Dashboard */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Sensor Data</h2>
          <SensorDashboard status={twinStatus} />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        {/* Predictions */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Recent Predictions</h2>
          {predictions.length > 0 ? (
            <div className="space-y-2">
              {predictions.map((pred, idx) => (
                <PredictionCard key={idx} prediction={pred} />
              ))}
            </div>
          ) : (
            <p className="text-gray-500">No predictions yet</p>
          )}
        </div>

        {/* Treatment Optimizer */}
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h2 className="text-xl font-semibold mb-4">Treatment Recommendations</h2>
          <TreatmentOptimizer />
        </div>
      </div>

      {/* Prediction Form */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Make New Prediction</h2>
        <PredictionForm />
      </div>
    </div>
  )
}

