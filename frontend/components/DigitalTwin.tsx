'use client'

import { useEffect, useRef } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Text } from '@react-three/drei'
import * as THREE from 'three'

// Water flow animation component
function AnimatedWater({ position, scale, turbidity }: any) {
  const meshRef = useRef<THREE.Mesh>(null)
  
  useEffect(() => {
    if (meshRef.current) {
      const material = meshRef.current.material as THREE.MeshStandardMaterial
      material.color.setHex(turbidity > 60 ? 0xff4444 : turbidity > 30 ? 0xffaa00 : 0x10b981)
    }
  }, [turbidity])

  return (
    <mesh ref={meshRef} position={position} scale={scale}>
      <cylinderGeometry args={[1.3, 1.3, 3.5, 64]} />
      <meshStandardMaterial 
        color={turbidity > 60 ? '#ff4444' : turbidity > 30 ? '#ffaa00' : '#10b981'}
        metalness={0.3}
        roughness={0.4}
        emissive={turbidity > 60 ? '#ff2222' : '#000000'}
        emissiveIntensity={turbidity > 60 ? 0.3 : 0}
      />
    </mesh>
  )
}

// Pipe connector
function Pipe({ from, to, color = '#60a5fa' }: any) {
  const length = Math.hypot(to[0] - from[0], to[2] - from[2])
  const mid = [(from[0] + to[0]) / 2, (from[1] + to[1]) / 2, (from[2] + to[2]) / 2]
  const angle = Math.atan2(to[2] - from[2], to[0] - from[0])

  return (
    <mesh position={mid as any} rotation={[0, angle, 0]}>
      <cylinderGeometry args={[0.25, 0.25, length, 16]} />
      <meshStandardMaterial color={color} metalness={0.6} roughness={0.2} />
    </mesh>
  )
}

// Treatment tank with label
function TreatmentTank({ position, size, color, label, value }: any) {
  return (
    <group>
      {/* Main tank */}
      <mesh position={position}>
        <cylinderGeometry args={[size, size, 3.5, 32]} />
        <meshStandardMaterial 
          color={color}
          metalness={0.4}
          roughness={0.3}
          wireframe={false}
        />
      </mesh>
      
      {/* Tank outline */}
      <mesh position={position}>
        <cylinderGeometry args={[size, size, 3.5, 32]} />
        <meshStandardMaterial 
          color="#ffffff"
          wireframe={true}
          transparent={true}
          opacity={0.2}
        />
      </mesh>

      {/* Label text */}
      <Text
        position={[position[0], position[1] + 3, position[2]]}
        fontSize={0.6}
        color="#ffffff"
        anchorX="center"
        anchorY="middle"
      >
        {label}
      </Text>

      {/* Value display */}
      <Text
        position={[position[0], position[1] - 2.5, position[2]]}
        fontSize={0.4}
        color="#00ff00"
        anchorX="center"
        anchorY="middle"
      >
        {value}
      </Text>
    </group>
  )
}

// Aeration equipment
function AerationTank({ position }: any) {
  const bubbleRefs = useRef<THREE.Mesh[]>([])

  useEffect(() => {
    const interval = setInterval(() => {
      bubbleRefs.current.forEach((bubble) => {
        if (bubble) {
          bubble.position.y += 0.02
          if (bubble.position.y > position[1] + 2) {
            bubble.position.y = position[1] - 1.5
          }
        }
      })
    }, 30)
    return () => clearInterval(interval)
  }, [position])

  return (
    <group>
      {/* Aeration basin */}
      <mesh position={position}>
        <boxGeometry args={[2.5, 3.5, 2]} />
        <meshStandardMaterial color="#8b5cf6" metalness={0.3} roughness={0.4} />
      </mesh>

      {/* Animated bubbles */}
      {Array.from({ length: 8 }).map((_, i) => (
        <mesh
          key={i}
          ref={(el) => {
            if (el) bubbleRefs.current[i] = el
          }}
          position={[
            position[0] + (Math.random() - 0.5) * 2,
            position[1] + Math.random() * 2,
            position[2] + (Math.random() - 0.5) * 1.5
          ]}
        >
          <sphereGeometry args={[0.15, 8, 8]} />
          <meshStandardMaterial color="#87ceeb" transparent opacity={0.6} />
        </mesh>
      ))}
    </group>
  )
}

export default function DigitalTwin({ status }: { status: any }) {
  const turbidity = status?.twin_state?.turbidity || 30
  const quality = status?.twin_state?.quality || 50
  const pressure = status?.twin_state?.pressure || 1.0

  return (
    <div className="w-full h-full bg-gradient-to-b from-slate-900 to-slate-800 rounded-lg overflow-hidden">
      <Canvas camera={{ position: [15, 12, 15], fov: 45 }}>
        {/* Lighting */}
        <ambientLight intensity={0.6} />
        <directionalLight position={[15, 20, 10]} intensity={1.2} castShadow />
        <pointLight position={[-10, 15, 0]} intensity={0.8} color="#60a5fa" />
        <pointLight position={[10, 15, 0]} intensity={0.8} color="#10b981" />
        <hemisphereLight groundColor="#444" intensity={0.4} />

        {/* Ground plane */}
        <mesh rotation={[-Math.PI / 2, 0, 0]} position={[0, -2, 0]}>
          <planeGeometry args={[30, 30]} />
          <meshStandardMaterial color="#2d2d3d" />
        </mesh>

        {/* STAGE 1: PRIMARY TREATMENT (Screening & Settling) */}
        <TreatmentTank
          position={[-8, 0, 0]}
          size={1.2}
          color="#3b82f6"
          label="PRIMARY"
          value="Settling"
        />

        {/* STAGE 2: SECONDARY TREATMENT (Aeration) */}
        <AerationTank position={[0, 0, 0]} />

        {/* STAGE 3: TERTIARY TREATMENT (Filtration) */}
        <TreatmentTank
          position={[8, 0, 0]}
          size={1}
          color={turbidity > 60 ? '#ef4444' : '#10b981'}
          label="TERTIARY"
          value={`Quality: ${quality}%`}
        />

        {/* OUTLET/FINAL TANK */}
        <mesh position={[14, 0, 0]}>
          <boxGeometry args={[1.5, 2.5, 1.5]} />
          <meshStandardMaterial color="#06b6d4" metalness={0.5} roughness={0.2} />
        </mesh>

        {/* Flow Direction: Inlet */}
        <Text position={[-12, 2, 0]} fontSize={0.5} color="#00ff00">
          INLET
        </Text>

        {/* Pipes connecting stages */}
        <Pipe from={[-6.5, 0.5, 0]} to={[-1, 0.5, 0]} color="#60a5fa" />
        <Pipe from={[1, 0.5, 0]} to={[6.5, 0.5, 0]} color="#60a5fa" />
        <Pipe from={[7.5, 0.5, 0]} to={[13, 0.5, 0]} color="#60a5fa" />

        {/* Status indicators */}
        <Text position={[0, 5, 0]} fontSize={0.8} color="#fff">
          TURBIDITY: {turbidity.toFixed(1)}%
        </Text>
        <Text position={[0, 4.2, 0]} fontSize={0.8} color={turbidity > 60 ? '#ff4444' : '#10b981'}>
          {turbidity > 60 ? '🔴 ALERT' : '🟢 NORMAL'}
        </Text>

        <Text position={[0, 3.2, 0]} fontSize={0.6} color="#60a5fa">
          Pressure: {pressure.toFixed(2)} bar
        </Text>

        {/* Control panel */}
        <mesh position={[-14, 2, 0]}>
          <boxGeometry args={[2, 3, 0.2]} />
          <meshStandardMaterial color="#1a1a2e" metalness={0.8} roughness={0.1} />
        </mesh>

        <Text position={[-14, 3, 0.15]} fontSize={0.4} color="#00ff00">
          CONTROL
        </Text>

        {/* Sludge tank (bottom) */}
        <mesh position={[0, -3, 0]}>
          <cylinderGeometry args={[1, 1.2, 1.5, 24]} />
          <meshStandardMaterial color="#8b4513" metalness={0.2} roughness={0.6} />
        </mesh>

        <Text position={[0, -4, 0]} fontSize={0.5} color="#d4af37">
          SLUDGE
        </Text>

        {/* Animations and interactivity */}
        <OrbitControls 
          enablePan={true} 
          enableZoom={true} 
          enableRotate={true}
          autoRotate={false}
          autoRotateSpeed={0}
        />
        
        {/* Grid helper */}
        <gridHelper args={[30, 30]} />
      </Canvas>

      {/* Status panel overlay */}
      <div className="absolute top-4 right-4 bg-black/70 p-4 rounded-lg text-white text-sm font-mono backdrop-blur">
        <div className="text-cyan-400">PLANT STATUS</div>
        <div className="text-green-400">✓ Primary: Active</div>
        <div className="text-green-400">✓ Secondary: Active</div>
        <div className={turbidity > 60 ? 'text-red-400' : 'text-green-400'}>
          {turbidity > 60 ? '✗ Tertiary: Alert' : '✓ Tertiary: Active'}
        </div>
      </div>

      {/* Legend */}
      <div className="absolute bottom-4 left-4 bg-black/70 p-3 rounded-lg text-xs text-white backdrop-blur">
        <div className="text-blue-400 mb-2">TREATMENT STAGES</div>
        <div className="text-blue-300">█ Primary: Settling</div>
        <div className="text-purple-300">█ Secondary: Aeration</div>
        <div className="text-green-300">█ Tertiary: Filtration</div>
        <div className="text-cyan-300">█ Outlet: Final Discharge</div>
      </div>
    </div>
  )
}

