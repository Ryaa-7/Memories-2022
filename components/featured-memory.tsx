'use client'

import { useState } from 'react'
import Image from 'next/image'
import { Heart, MapPin, Calendar } from 'lucide-react'
import { Reveal } from '@/components/reveal'
import { cn } from '@/lib/utils'
import { useMemories } from '@/lib/use-memories'

export function FeaturedMemory() {
  const [loved, setLoved] = useState(true)
  const { photos } = useMemories()
  const featuredSrc = photos[1]?.src || photos[0]?.src || '/memories/featured.png'

  return (
    <section id="about" className="relative mx-auto max-w-6xl scroll-mt-24 px-5 py-24">
      <Reveal className="mb-12 text-center">
        <p className="font-sans text-sm font-medium uppercase tracking-[0.3em] text-primary">
          Featured
        </p>
        <h2 className="mt-3 text-balance font-serif text-4xl font-semibold text-foreground md:text-5xl">
          A Moment Worth Remembering
        </h2>
      </Reveal>

      <Reveal className="grid items-center gap-10 md:grid-cols-2">
        {/* image with floating frame */}
        <div className="animate-float-slow relative">
          <div className="film-grain relative aspect-[4/5] overflow-hidden rounded-[2rem] shadow-2xl shadow-primary/25">
            <Image
              src={featuredSrc}
              alt="Featured memory"
              fill
              sizes="(max-width: 768px) 100vw, 50vw"
              unoptimized
              className="object-cover"
            />
            <span className="pointer-events-none absolute inset-0 rounded-[2rem] ring-1 ring-inset ring-white/30" />
            <span className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_60%,oklch(0.4_0.06_250/0.35)_100%)]" />
          </div>
          {/* soft glow behind */}
          <div className="absolute -inset-4 -z-10 rounded-[2.5rem] bg-primary/25 blur-3xl" />
        </div>

        {/* details */}
        <div className="text-center md:text-left">
          <div className="flex flex-wrap justify-center gap-4 md:justify-start">
            <span className="inline-flex items-center gap-2 text-sm font-medium text-muted-foreground">
              <Calendar className="h-4 w-4 text-primary" />
              December 31, 2024
            </span>
            <span className="inline-flex items-center gap-2 text-sm font-medium text-muted-foreground">
              <MapPin className="h-4 w-4 text-primary" />
              By the old lighthouse
            </span>
          </div>

          <h3 className="mt-5 text-balance font-serif text-3xl font-semibold leading-tight text-foreground md:text-4xl">
            The night we wrote our wishes in the sparks
          </h3>

          <p className="mx-auto mt-4 max-w-md text-pretty leading-relaxed text-muted-foreground md:mx-0">
            The air was cold and everything was quiet except our laughter. We held
            the sparklers up to the dark and, for a moment, it felt like the whole
            sky belonged to us. Some memories don&apos;t fade — they just glow softer
            with time.
          </p>

          <button
            type="button"
            onClick={() => setLoved((v) => !v)}
            className="glass mx-auto mt-7 inline-flex items-center gap-2 rounded-full px-5 py-3 text-sm font-medium text-foreground transition-transform hover:scale-105 md:mx-0"
          >
            <Heart
              className={cn(
                'h-4 w-4 transition-colors',
                loved ? 'animate-heart-pop fill-rose-400 text-rose-400' : 'text-foreground/70',
              )}
            />
            {loved ? 'One of our favorites' : 'Add to favorites'}
          </button>
        </div>
      </Reveal>
    </section>
  )
}
