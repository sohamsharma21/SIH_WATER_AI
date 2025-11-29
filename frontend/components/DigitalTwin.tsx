'use client'

import { useEffect, useRef, useState } from 'react'
import type { PlantStatus } from '@/lib/types'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Text } from '@react-three/drei'
import * as THREE from 'three'

// Water flow animation component
type Vec3 = [number, number, number]

function AnimatedWater({ position, scale, turbidity }: { position: Vec3, scale?: Vec3 | number, turbidity: number }) {
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
function Pipe({ from, to, color = '#60a5fa' }: { from: Vec3, to: Vec3, color?: string }) {
  const length = Math.hypot(to[0] - from[0], to[2] - from[2])
  const mid = [(from[0] + to[0]) / 2, (from[1] + to[1]) / 2, (from[2] + to[2]) / 2]
  const angle = Math.atan2(to[2] - from[2], to[0] - from[0])

  return (
    <mesh position={mid as Vec3} rotation={[0, angle, 0]}>
      <cylinderGeometry args={[0.25, 0.25, length, 16]} />
      <meshStandardMaterial color={color} metalness={0.6} roughness={0.2} />
    </mesh>
  )
}

// Treatment tank with label
function TreatmentTank({ position, size, color, label, value, onHover, onPointerDown, isSelected }: { position: Vec3, size: number, color: string, label: string, value?: string | number, onHover?: (label: string | null) => void, onPointerDown?: () => void, isSelected?: boolean }) {
  const ringRef = useRef<THREE.Mesh | null>(null)
  // pulse selected ring
  useFrame((state, delta) => {
    if (isSelected && ringRef.current) {
      const s = 1 + Math.sin(state.clock.getElapsedTime() * 2.5) * 0.06
      ringRef.current.scale.set(s, 1, s)
    }
  })

  return (
    <group onPointerOver={() => onHover?.(label)} onPointerOut={() => onHover?.(null)} onPointerDown={onPointerDown}>
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

      {/* Selection ring */}
      {isSelected && (
        <mesh ref={ringRef} position={[position[0], position[1] - 1.4, position[2]]}>
          <torusGeometry args={[size + 0.6, 0.07, 12, 64]} />
          <meshStandardMaterial color="#60a5fa" emissive="#60a5fa" emissiveIntensity={0.6} transparent opacity={0.9} />
        </mesh>
      )}
    </group>
  )
}

// Aeration equipment
function AerationTank({ position, onHover }: { position: Vec3, onHover?: (label: string | null) => void }) {
  const bubbleRefs = useRef<Array<THREE.Mesh | null>>([])

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
    <group onPointerOver={() => onHover?.('SECONDARY')} onPointerOut={() => onHover?.(null)}>
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

import { api } from '@/lib/api'
import DigitalTwinPanel from './DigitalTwinPanel'
import useTwinRealtime from '@/hooks/useTwinRealtime'

export default function DigitalTwin({ status }: { status?: PlantStatus | null }) {
  const [hoverLabel, setHoverLabel] = useState<string | null>(null)
  const [autoRotate, setAutoRotate] = useState(false)
  const controlsRef = useRef<any>(null)
  // Live twin data state — switch to realtime hook (supabase) and accept Dashboard prop updates
  const realtime = useTwinRealtime(status ?? null)
  const [twinState, setTwinState] = useState<any>(status ?? realtime.twinState ?? null)
  const [selectedKey, setSelectedKey] = useState<string | null>(null)

  const turbidity = Number(twinState?.twin_state?.turbidity ?? status?.twin_state?.turbidity ?? 30)
  const quality = Number(twinState?.twin_state?.quality ?? status?.twin_state?.quality ?? 50)
  const pressure = Number(twinState?.twin_state?.pressure ?? status?.twin_state?.pressure ?? 1.0)

  // Keep twinState synced with realtime hook & prop updates
  useEffect(() => {
    if (realtime?.twinState) setTwinState(realtime.twinState)
  }, [realtime?.twinState])

  useEffect(() => {
    // if Dashboard updated the `status` prop, apply it immediately
    if (status) setTwinState(status)
  }, [status])

  // Prevent uncontrolled expansion: provide an explicit responsive height for the twin canvas
  return (
    <div className="w-full h-[52vh] md:h-[64vh] lg:h-[72vh] bg-gradient-to-b from-slate-900 to-slate-800 rounded-lg overflow-hidden relative">
      <Canvas className="w-full h-full" camera={{ position: [18, 14, 18], fov: 50 }}>
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
          onHover={(label) => setHoverLabel(label)}
          onPointerDown={() => setSelectedKey('PRIMARY')}
          isSelected={selectedKey === 'PRIMARY'}
        />

        {/* STAGE 2: SECONDARY TREATMENT (Aeration) */}
        <AerationTank position={[0, 0, 0]} onHover={(label) => { setHoverLabel(label); }} />

        {/* STAGE 3: TERTIARY TREATMENT (Filtration) */}
        <TreatmentTank
          position={[8, 0, 0]}
          size={1}
          color={turbidity > 60 ? '#ef4444' : '#10b981'}
          label="TERTIARY"
          value={`Quality: ${quality}%`}
          onHover={(label) => { setHoverLabel(label); }}
          onPointerDown={() => setSelectedKey('TERTIARY')}
          isSelected={selectedKey === 'TERTIARY'}
        />

        {/* OUTLET/FINAL TANK */}
        <mesh position={[14, 0, 0]} onPointerOver={() => setHoverLabel('OUTLET')} onPointerOut={() => setHoverLabel(null)} onPointerDown={() => setSelectedKey('OUTLET')}>
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
        <mesh position={[0, -3, 0]} onPointerOver={() => setHoverLabel('SLUDGE')} onPointerOut={() => setHoverLabel(null)} onPointerDown={() => setSelectedKey('SLUDGE')}>
          <cylinderGeometry args={[1, 1.2, 1.5, 24]} />
          <meshStandardMaterial color="#8b4513" metalness={0.2} roughness={0.6} />
        </mesh>

        <Text position={[0, -4, 0]} fontSize={0.5} color="#d4af37">
          SLUDGE
        </Text>

        {/* Animations and interactivity */}
        <OrbitControls
          ref={controlsRef}
          enablePan={true}
          enableZoom={true}
          enableRotate={true}
          minDistance={8}
          maxDistance={60}
          minPolarAngle={Math.PI / 8}
          maxPolarAngle={Math.PI / 2.1}
          enableDamping={true}
          dampingFactor={0.07}
          autoRotate={autoRotate}
          autoRotateSpeed={autoRotate ? 0.6 : 0}
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

      {/* Hover label */}
      {hoverLabel && (
        <div className="absolute left-6 top-6 bg-gradient-to-r from-white/5 via-white/3 to-black/10 px-3 py-2 rounded-md text-sm text-white backdrop-blur border border-white/5 shadow-lg">
          <div className="text-xs text-slate-300">{hoverLabel}</div>
          <div className="mt-1 font-semibold text-white text-lg">
            {(() => {
              // attempt to show live value for hovered label
              const sensor = (twinState?.sensor_status || {})[hoverLabel]
              if (sensor) return `${Number(sensor.current_value ?? sensor.value).toFixed(2)} ${sensor.unit || ''}`
              // fallback for prediction fields
              if (twinState?.latest_prediction && twinState.latest_prediction.prediction && hoverLabel === 'TERTIARY') {
                return `${twinState.latest_prediction.prediction.quality_score || twinState.latest_prediction.prediction.prediction}`
              }
              return '—'
            })()}
          </div>
          <div className="text-xs text-slate-400">{(() => {
            const sensor = (twinState?.sensor_status || {})[hoverLabel]
            return sensor?.timestamp ? new Date(sensor.timestamp).toLocaleString() : ''
          })()}</div>
        </div>
      )}

      {/* Controls overlay */}
      <div className="absolute top-4 left-4 flex gap-2">
        <button
          className="px-3 py-1 rounded bg-slate-700/60 text-white text-sm hover:bg-slate-600"
          onClick={() => {
            // reset camera
            if (controlsRef.current) {
              try { controlsRef.current.reset() } catch { /* noop */ }
            }
          }}
        >Reset view</button>

        <button
          className={`px-3 py-1 rounded text-sm ${autoRotate ? 'bg-emerald-600' : 'bg-slate-700/60'} text-white hover:opacity-90`}
          onClick={() => setAutoRotate((s) => !s)}
        >{autoRotate ? 'Auto-rotating' : 'Toggle rotate'}</button>
      </div>

      {/* Right side details panel - visible when user clicks a region */}
      <div className={`absolute top-0 right-0 h-full w-0 md:w-96 transition-all duration-300 ${selectedKey ? 'w-96 bg-gradient-to-tl from-slate-900/90 via-slate-800/80 to-slate-700/80 p-4' : ''}`}>
        {selectedKey ? (
          <div className="h-full flex flex-col gap-4 text-sm text-white">
            <div className="flex justify-between items-center">
              <div className="text-lg font-semibold">Details — {selectedKey}</div>
              <button className="px-2 py-1 text-xs bg-slate-600/40 rounded" onClick={() => setSelectedKey(null)}>Close</button>
            </div>

            <div className="flex-1 overflow-auto">
              {/* Sensor summary */}
              <div className="mb-4">
                <div className="text-xs text-slate-300">Live sensors</div>
                <div className="mt-2 space-y-2">
                  {Object.entries(twinState?.sensor_status || {}).map(([k,v]: any) => (
                    <div key={k} className="p-2 bg-white/5 rounded flex justify-between items-center">
                      <div>
                        <div className="font-semibold">{k}</div>
                        <div className="text-xs text-slate-400">{String(v.unit || '')} • {v.timestamp ? new Date(v.timestamp).toLocaleString() : '—'}</div>
                      </div>
                      <div className="text-2xl font-bold text-cyan-300">{Number(v.current_value ?? v.value).toFixed(2)}</div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Mini-trends: fetch recent sensor history for clicked item */}
              <div>
                <div className="text-xs text-slate-300">Recent trends</div>
                {/* Trend chart will load below */}
                <DigitalTwinPanel selectedKey={selectedKey} twinData={twinState} />
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  )
}

