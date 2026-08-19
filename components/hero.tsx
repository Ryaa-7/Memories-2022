'use client'

import { useEffect, useState } from 'react'
import Image from 'next/image'
import { ChevronDown, Play, Sparkles } from 'lucide-react'
import { useMemories } from '@/lib/use-memories'

export function Hero() {
  const [offset, setOffset] = useState(0)
  const { photos } = useMemories()
  const heroSrc = photos[0]?.src || '/memories/hero.png'

  useEffect(() => {
    let raf = 0
    const onScroll = () => {
      raf = requestAnimationFrame(() => setOffset(window.scrollY))
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => {
      window.removeEventListener('scroll', onScroll)
      cancelAnimationFrame(raf)
    }
  }, [])

  return (
    <section
      id="home"
      className="film-grain relative flex min-h-screen items-center justify-center overflow-hidden"
    >
      {/* parallax background image */}
      <div
        className="absolute inset-0 -z-10 will-change-transform"
        style={{ transform: `translateY(${offset * 0.35}px) scale(1.15)` }}
      >
        <Image
          src={heroSrc}
          alt="Memories"
          fill
          priority
          unoptimized
          className="animate-slow-zoom object-cover"
        />
      </div>

      {/* soft blue overlay + blur */}
      <div className="absolute inset-0 -z-10 bg-gradient-to-b from-[oklch(0.7_0.08_245)]/45 via-[oklch(0.8_0.06_235)]/35 to-[oklch(0.98_0.012_240)]" />
      <div className="absolute inset-0 -z-10 backdrop-blur-[2px]" />

      <div
        className="mx-auto max-w-3xl px-6 text-center"
        style={{ transform: `translateY(${offset * -0.15}px)`, opacity: Math.max(0, 1 - offset / 600) }}
      >
        <span className="glass mx-auto mb-6 inline-flex items-center gap-2 rounded-full px-4 py-1.5 text-sm font-medium text-foreground/80">
          <Sparkles className="h-4 w-4 text-primary" />
          A beautiful digital memory book
        </span>

        <h1 className="text-balance font-serif text-6xl font-semibold leading-[0.95] tracking-tight text-white text-glow drop-shadow-sm sm:text-7xl md:text-8xl">
          NGOBOK
        </h1>

        <p className="mx-auto mt-6 max-w-xl text-pretty text-lg font-light leading-relaxed text-white/90 md:text-xl">
          Little moments, beautiful memories, forever.
        </p>

        <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <a
            href="#memories"
            className="group inline-flex items-center gap-2 rounded-full bg-primary px-7 py-3.5 text-base font-medium text-primary-foreground shadow-lg shadow-primary/40 transition-all hover:scale-105 hover:shadow-xl hover:shadow-primary/50"
          >
            Explore Memories
          </a>
          <a
            href="#videos"
            className="glass inline-flex items-center gap-2 rounded-full px-7 py-3.5 text-base font-medium text-foreground transition-all hover:scale-105"
          >
            <Play className="h-4 w-4 fill-primary text-primary" />
            Watch Our Story
          </a>
        </div>
      </div>

      {/* scroll indicator */}
      <a
        href="#memories"
        aria-label="Scroll down"
        className="absolute bottom-8 left-1/2 -translate-x-1/2 text-white/80"
      >
        <span className="animate-bounce-soft flex h-11 w-7 items-start justify-center rounded-full border-2 border-white/60 p-1.5">
          <ChevronDown className="h-4 w-4" />
        </span>
      </a>
    </section>
  )
}
