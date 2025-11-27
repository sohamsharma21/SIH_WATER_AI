'use client'

import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { motion } from 'framer-motion'

export default function LandingPage() {
  const router = useRouter()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="container mx-auto px-4 py-6">
        <nav className="flex justify-between items-center">
          <div className="text-2xl font-bold text-blue-700">SIH WATER AI</div>
          <div className="space-x-4">
            <Link href="/login" className="text-blue-700 hover:text-blue-900">
              Login
            </Link>
            <Link
              href="/signup"
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
            >
              Sign Up
            </Link>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="container mx-auto px-4 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-4xl mx-auto"
        >
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            AI-Powered Industrial
            <br />
            <span className="text-blue-600">Wastewater Treatment</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Optimize your wastewater treatment plant with multi-model AI,
            real-time monitoring, and 3D digital twin visualization.
          </p>
          <div className="flex justify-center gap-4">
            <button
              onClick={() => router.push('/signup')}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-blue-700 transition"
            >
              Get Started
            </button>
            <button
              onClick={() => router.push('/dashboard')}
              className="bg-white text-blue-600 px-8 py-3 rounded-lg text-lg font-semibold border-2 border-blue-600 hover:bg-blue-50 transition"
            >
              View Demo
            </button>
          </div>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="grid md:grid-cols-3 gap-8 mt-20"
        >
          <FeatureCard
            title="Multi-Model AI"
            description="4 trained ML models for accurate predictions and treatment optimization"
            icon="🤖"
          />
          <FeatureCard
            title="Digital Twin"
            description="3D real-time visualization of your treatment plant with live sensor data"
            icon="🌐"
          />
          <FeatureCard
            title="Real-time Monitoring"
            description="MQTT sensor ingestion with instant alerts and recommendations"
            icon="📊"
          />
        </motion.div>
      </main>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 text-center text-gray-600">
        <p>© 2024 SIH WATER AI - Team Nova_Minds</p>
      </footer>
    </div>
  )
}

function FeatureCard({
  title,
  description,
  icon,
}: {
  title: string
  description: string
  icon: string
}) {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      className="bg-white p-6 rounded-xl shadow-lg"
    >
      <div className="text-4xl mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </motion.div>
  )
}

