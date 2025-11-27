'use client'

import { useState } from 'react'
import { api } from '@/lib/api'

export default function PredictionForm() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [modelName, setModelName] = useState('dataset2')
  const [features, setFeatures] = useState({
    ph: 7.0,
    Hardness: 200.0,
    Solids: 20000.0,
    Chloramines: 7.0,
    Sulfate: 300.0,
    Conductivity: 400.0,
    Organic_carbon: 10.0,
    Trihalomethanes: 50.0,
    Turbidity: 3.0,
  })

  const handlePredict = async () => {
    setLoading(true)
    setResult(null)
    try {
      const response = await api.predict({
        features,
        model_name: modelName,
        use_ensemble: false,
      })

      setResult(response.data)
    } catch (error: any) {
      console.error('Error making prediction:', error)
      alert(`Error: ${error.response?.data?.detail || error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">Model</label>
        <select
          value={modelName}
          onChange={(e) => setModelName(e.target.value)}
          className="w-full px-3 py-2 border rounded-lg"
        >
          <option value="dataset2">Dataset 2 - Water Potability</option>
          <option value="dataset3">Dataset 3 - UCI Treatment</option>
          <option value="dataset4">Dataset 4 - Melbourne WWTP</option>
        </select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {Object.entries(features).map(([key, value]) => (
          <div key={key}>
            <label className="block text-sm font-medium mb-1">{key}</label>
            <input
              type="number"
              value={value}
              onChange={(e) =>
                setFeatures({ ...features, [key]: parseFloat(e.target.value) || 0 })
              }
              className="w-full px-3 py-2 border rounded-lg"
              step="0.1"
            />
          </div>
        ))}
      </div>

      <button
        onClick={handlePredict}
        disabled={loading}
        className="w-full bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? 'Predicting...' : 'Make Prediction'}
      </button>

      {result && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold mb-2">Prediction Result</h3>
          <div className="space-y-2 text-sm">
            <div>
              <span className="font-medium">Model:</span>{' '}
              {result.prediction?.model_name || 'Unknown'}
            </div>
            <div>
              <span className="font-medium">Prediction:</span>{' '}
              {result.prediction?.prediction?.toFixed(2) || 'N/A'}
            </div>
            <div>
              <span className="font-medium">Quality Score:</span>{' '}
              <span className="text-green-600">
                {result.prediction?.quality_score?.toFixed(2) || 'N/A'}%
              </span>
            </div>
            <div>
              <span className="font-medium">Contamination Index:</span>{' '}
              <span className="text-red-600">
                {result.prediction?.contamination_index?.toFixed(2) || 'N/A'}%
              </span>
            </div>
            {result.prediction?.confidence && (
              <div>
                <span className="font-medium">Confidence:</span>{' '}
                {(result.prediction.confidence * 100).toFixed(1)}%
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

