'use client'

export default function SensorDashboard({ status }: { status: any }) {
  const sensorStatus = status?.sensor_status || {}

  if (Object.keys(sensorStatus).length === 0) {
    return <p className="text-gray-500">No sensor data available</p>
  }

  return (
    <div className="space-y-4">
      {Object.entries(sensorStatus).map(([param, data]: [string, any]) => (
        <div key={param} className="border-b pb-4">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-semibold capitalize">{param.replace('_', ' ')}</h3>
              <p className="text-sm text-gray-500">
                {data.unit} • {new Date(data.timestamp).toLocaleTimeString()}
              </p>
            </div>
            <div className="text-2xl font-bold text-blue-600">
              {data.current_value?.toFixed(2)}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

