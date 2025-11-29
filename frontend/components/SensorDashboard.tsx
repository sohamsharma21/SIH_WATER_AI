'use client'

import type { PlantStatus, SensorData } from '@/lib/types'

export default function SensorDashboard({ status }: { status?: PlantStatus | null }) {
  const sensorStatus: Record<string, Partial<SensorData>> = (status?.sensor_status as Record<string, Partial<SensorData>> ) || {}

  if (Object.keys(sensorStatus).length === 0) {
    return <p className="text-gray-500">No sensor data available</p>
  }

  return (
    <div className="space-y-4">
      {Object.entries(sensorStatus).map(([param, data]: [string, Partial<SensorData>]) => (
        <div key={param} className="border-b pb-4">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-semibold capitalize">{param.replace('_', ' ')}</h3>
              <p className="text-sm text-gray-500">
                {data.unit} • {data.timestamp ? new Date(data.timestamp).toLocaleTimeString() : '—'}
              </p>
            </div>
            <div className="text-2xl font-bold text-blue-600">
              {typeof data.current_value === 'number' ? data.current_value.toFixed(2) : data.value?.toFixed?.(2) ?? '-'}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

