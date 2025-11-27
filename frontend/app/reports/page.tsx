'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api'

export default function ReportsPage() {
  const [reports, setReports] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [generating, setGenerating] = useState(false)

  const generateReport = async () => {
    setGenerating(true)
    try {
      const response = await api.generateReport({
        sensor_data: {},
      })

      if (response.data.report_url) {
        window.open(response.data.report_url, '_blank')
        loadReports()
      }
    } catch (error) {
      console.error('Error generating report:', error)
      alert('Failed to generate report')
    } finally {
      setGenerating(false)
    }
  }

  const loadReports = async () => {
    // This would fetch reports from database
    // For now, placeholder
    setReports([])
  }

  useEffect(() => {
    loadReports()
  }, [])

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Reports</h1>
        <button
          onClick={generateReport}
          disabled={generating}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
        >
          {generating ? 'Generating...' : 'Generate New Report'}
        </button>
      </div>

      {reports.length === 0 ? (
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <p className="text-gray-500 mb-4">No reports generated yet</p>
          <button
            onClick={generateReport}
            disabled={generating}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Generate First Report
          </button>
        </div>
      ) : (
        <div className="grid gap-4">
          {reports.map((report, idx) => (
            <div key={idx} className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-semibold mb-2">{report.report_name}</h3>
              <p className="text-gray-600 mb-4">
                Generated: {new Date(report.generated_at).toLocaleString()}
              </p>
              {report.public_url && (
                <a
                  href={report.public_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:underline"
                >
                  View Report →
                </a>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

