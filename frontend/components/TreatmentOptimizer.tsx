'use client'

import { useState } from 'react'
import type { PredictionWithOptimization } from '@/lib/types'
import { api } from '@/lib/api'

export default function TreatmentOptimizer() {
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState<any | null>(null)

  const handleOptimize = async () => {
    setLoading(true)
    try {
      // Use dataset2 features for prediction
      const response = await api.predict({
        features: {
          ph: 7.2,
          Hardness: 200.0,
          Solids: 20000.0,
          Chloramines: 7.0,
          Sulfate: 300.0,
          Conductivity: 400.0,
          Organic_carbon: 10.0,
          Trihalomethanes: 50.0,
          Turbidity: 3.0,
        },
        model_name: 'dataset2',
        target_quality: 'environmental',
      })

      if (response.data.optimization) {
        // backend may return either a structured optimization object or an array
        // normalize to a single object when possible
        setResults(response.data.optimization ?? response.data)
      } else if (response.data.prediction) {
        // If no optimization, show prediction results
        setResults({
          prediction: response.data.prediction,
          quality_score: response.data.prediction.quality_score,
          contamination_index: response.data.prediction.contamination_index,
        })
      }
    } catch (error: unknown) {
      console.error('Error optimizing:', error)
      alert('Error running optimization. Make sure backend is running.')
    } finally {
      setLoading(false)
    }
  }

  if (!results) {
    return (
      <div className="text-center">
        <button
          onClick={handleOptimize}
          disabled={loading}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Optimizing...' : 'Run Optimization'}
        </button>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="border rounded p-4 bg-blue-50">
        <h4 className="font-semibold mb-2">Primary Treatment</h4>
        <ul className="text-sm space-y-1">
          <li>Settling Time: {results.primary_treatment?.settling_time_min} min</li>
          <li>Coagulant Dose: {results.primary_treatment?.coagulant_dose_ml} mL</li>
        </ul>
      </div>

      <div className="border rounded p-4 bg-green-50">
        <h4 className="font-semibold mb-2">Secondary Treatment</h4>
        <ul className="text-sm space-y-1">
          <li>Aeration Time: {results.secondary_treatment?.aeration_time_min} min</li>
          <li>DO Target: {results.secondary_treatment?.do_target_ppm} ppm</li>
        </ul>
      </div>

      <div className="border rounded p-4 bg-yellow-50">
        <h4 className="font-semibold mb-2">Final Reuse</h4>
        <p className="text-sm">
          Type: {results.final_reuse?.reuse_type}
          <br />
          Recovery: {results.final_reuse?.recovery_percentage}%
        </p>
      </div>

      <button
        onClick={() => setResults(null)}
        className="text-blue-600 hover:underline text-sm"
      >
        Reset
      </button>
    </div>
  )
}

