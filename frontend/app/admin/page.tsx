'use client'

import { useState, useEffect } from 'react'
import type { ModelInfo } from '@/lib/types'
import { api } from '@/lib/api'

export default function AdminPage() {
  const [models, setModels] = useState<ModelInfo[]>([])
  const [loading, setLoading] = useState(true)
  const [training, setTraining] = useState(false)

  useEffect(() => {
    loadModels()
  }, [])

  const loadModels = async () => {
    try {
      const response = await api.getModels()
      // Combine manager models and database models
      const managerModels: ModelInfo[] = response.data.manager_models || []
      const dbModels: ModelInfo[] = response.data.database_models || []
      
      // Merge models, prefer database models if available
      const allModels: ModelInfo[] = [...dbModels]
      managerModels.forEach((mm: ModelInfo) => {
        if (!allModels.find((m: ModelInfo) => m.dataset_name === mm.dataset_name)) {
          allModels.push({
            dataset_name: mm.dataset_name,
            model_name: mm.dataset_name,
            model_type: mm.model_type,
            is_active: true,
            feature_columns: mm.feature_columns,
            target_column: mm.target_column,
          })
        }
      })
      
      setModels(allModels)
      setLoading(false)
    } catch (error) {
      console.error('Error loading models:', error)
      setLoading(false)
    }
  }

  const trainAllModels = async () => {
    setTraining(true)
    try {
      await api.trainAllModels()
      alert('Training started! This may take a while.')
      setTimeout(loadModels, 5000)
    } catch (error) {
      console.error('Error training models:', error)
      alert('Failed to start training')
    } finally {
      setTraining(false)
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="text-center">Loading models...</div>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Admin Panel</h1>
        <button
          onClick={trainAllModels}
          disabled={training}
          className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 disabled:opacity-50"
        >
          {training ? 'Training...' : 'Train All Models'}
        </button>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Available Models</h2>
        
        {models.length === 0 ? (
          <p className="text-gray-500">No models trained yet</p>
        ) : (
          <div className="space-y-4">
            {models.map((model, idx) => (
              <div key={idx} className="border rounded-lg p-4">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold">{model.model_name}</h3>
                    <p className="text-sm text-gray-600">
                      Dataset: {model.dataset_name} • Version: {model.model_version}
                    </p>
                    <p className="text-sm text-gray-600">
                      Type: {model.model_type} • Training Date: {model.training_date ? new Date(model.training_date).toLocaleDateString() : 'N/A'}
                    </p>
                  </div>
                  <div className="text-right">
                    {model.accuracy && (
                      <p className="text-sm">
                        <span className="font-semibold">Accuracy:</span> {(model.accuracy * 100).toFixed(2)}%
                      </p>
                    )}
                    {model.r2_score && (
                      <p className="text-sm">
                        <span className="font-semibold">R² Score:</span> {model.r2_score.toFixed(3)}
                      </p>
                    )}
                    <span className={`text-xs px-2 py-1 rounded ${
                      model.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                    }`}>
                      {model.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

