'use client'

import { useEffect, useState } from 'react'

interface Particle {
  left: number
  size: number
  delay: number
  duration: number
  kind: 'star' | 'bubble' | 'heart'
}

function makeParticles(count: number): Particle[] {
  const kinds: Particle['kind'][] = ['star', 'bubble', 'heart']
  return Array.from({ length: count }, (_, i) => ({
    left: Math.random() * 100,
    size: 4 + Math.random() * 10,
    delay: Math.random() * 12,
    duration: 10 + Math.random() * 14,
    kind: kinds[i % kinds.length],
  }))
}

export function AmbientBackground() {
  const [particles, setParticles] = useState<Particle[]>([])

  useEffect(() => {
    setParticles(makeParticles(22))
  }, [])

  return (
    <div aria-hidden="true" className="pointer-events-none fixed inset-0 -z-20 overflow-hidden">
      {/* soft blue gradient wash */}
      <div className="absolute inset-0 bg-gradient-to-b from-[oklch(0.98_0.012_240)] via-[oklch(0.96_0.02_235)] to-[oklch(0.99_0.008_240)]" />

      {/* drifting gradient blobs */}
      <div className="animate-drift absolute -left-32 top-10 h-[28rem] w-[28rem] rounded-full bg-[oklch(0.86_0.07_235)] opacity-40 blur-3xl" />
      <div
        className="animate-drift absolute -right-24 top-1/3 h-[32rem] w-[32rem] rounded-full bg-[oklch(0.83_0.09_250)] opacity-35 blur-3xl"
        style={{ animationDelay: '4s' }}
      />
      <div
        className="animate-drift absolute bottom-0 left-1/3 h-[26rem] w-[26rem] rounded-full bg-[oklch(0.9_0.05_220)] opacity-40 blur-3xl"
        style={{ animationDelay: '8s' }}
      />

      {/* floating particles */}
      {particles.map((p, i) => (
        <span
          key={i}
          className="absolute bottom-0 text-[oklch(0.72_0.11_240)]"
          style={{
            left: `${p.left}%`,
            width: p.size,
            height: p.size,
            animation: `float-particle ${p.duration}s linear ${p.delay}s infinite`,
          }}
        >
          {p.kind === 'star' && (
            <svg viewBox="0 0 24 24" fill="currentColor" className="h-full w-full opacity-70">
              <path d="M12 2l2.4 6.9L21 9.3l-5.2 4.3L17.6 21 12 17l-5.6 4 1.8-7.4L3 9.3l6.6-.4z" />
            </svg>
          )}
          {p.kind === 'bubble' && (
            <span className="block h-full w-full rounded-full border border-[oklch(0.72_0.11_240)]/50 bg-[oklch(0.85_0.08_235)]/30" />
          )}
          {p.kind === 'heart' && (
            <svg viewBox="0 0 24 24" fill="currentColor" className="h-full w-full opacity-60">
              <path d="M12 21s-7.5-4.9-10-9.2C.6 9 1.6 5.4 4.8 4.6 7 4 9 5.2 12 8c3-2.8 5-4 7.2-3.4 3.2.8 4.2 4.4 2.8 7.2C19.5 16.1 12 21 12 21z" />
            </svg>
          )}
        </span>
      ))}

      {/* vignette */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_55%,oklch(0.7_0.06_250/0.25)_100%)]" />
    </div>
  )
}
