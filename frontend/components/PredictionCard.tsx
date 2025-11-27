'use client'

export default function PredictionCard({ prediction }: { prediction: any }) {
  const qualityScore = prediction.quality_score || 0
  const contaminationIndex = prediction.contamination_index || 0

  const getQualityColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="border rounded-lg p-4 mb-4 bg-gray-50">
      <div className="flex justify-between items-start mb-2">
        <div>
          <h3 className="font-semibold">{prediction.model_name || 'Unknown Model'}</h3>
          <p className="text-sm text-gray-500">
            {new Date(prediction.timestamp).toLocaleString()}
          </p>
        </div>
        <div className={`text-2xl font-bold ${getQualityColor(qualityScore)}`}>
          {qualityScore.toFixed(1)}
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-2 text-sm">
        <div>
          <span className="text-gray-600">Quality Score:</span>
          <span className="ml-2 font-semibold">{qualityScore.toFixed(2)}/100</span>
        </div>
        <div>
          <span className="text-gray-600">Contamination:</span>
          <span className="ml-2 font-semibold">{contaminationIndex.toFixed(2)}/100</span>
        </div>
      </div>
    </div>
  )
}

