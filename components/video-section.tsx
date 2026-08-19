'use client'

import { useState } from 'react'
import Image from 'next/image'
import { Play, X, Clock } from 'lucide-react'
import { type Video } from '@/lib/memories-data'
import { useMemories } from '@/lib/use-memories'
import { Reveal } from '@/components/reveal'

export function VideoSection() {
  const { videos } = useMemories()
  const [selected, setSelected] = useState<Video | null>(null)

  if (videos.length === 0) return null

  return (
    <section id="videos" className="relative mx-auto max-w-6xl scroll-mt-24 px-5 py-24">
      <Reveal className="mb-12 text-center">
        <p className="font-sans text-sm font-medium uppercase tracking-[0.3em] text-primary">
          In Motion
        </p>
        <h2 className="mt-3 text-balance font-serif text-4xl font-semibold text-foreground md:text-5xl">
          Our Videos
        </h2>
        <p className="mx-auto mt-4 max-w-lg text-pretty leading-relaxed text-muted-foreground">
          Press play and step back into the days that still feel like yesterday.
        </p>
      </Reveal>

      <div className="grid gap-6 sm:grid-cols-2">
        {videos.map((video, i) => (
          <Reveal key={video.id} delay={i * 90}>
            <button
              type="button"
              onClick={() => setSelected(video)}
              className="group relative block aspect-video w-full overflow-hidden rounded-3xl text-left shadow-lg shadow-[oklch(0.72_0.11_240)]/15 outline-none ring-primary/50 transition-all duration-500 hover:shadow-2xl hover:shadow-primary/30 focus-visible:ring-2"
            >
              <Image
                src={video.thumbnail}
                alt={video.title}
                fill
                sizes="(max-width: 640px) 100vw, 50vw"
                className="object-cover transition-transform duration-700 group-hover:scale-110"
              />
              {/* cinematic gradient */}
              <span className="absolute inset-0 bg-gradient-to-t from-[oklch(0.35_0.06_250)]/85 via-transparent to-[oklch(0.6_0.06_245)]/20" />

              {/* play button */}
              <span className="absolute inset-0 flex items-center justify-center">
                <span className="glass flex h-16 w-16 items-center justify-center rounded-full transition-transform duration-500 group-hover:scale-110">
                  <Play className="h-6 w-6 translate-x-0.5 fill-primary text-primary" />
                </span>
              </span>

              {/* duration */}
              <span className="glass absolute right-3 top-3 inline-flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-medium text-foreground">
                <Clock className="h-3 w-3" />
                {video.duration}
              </span>

              {/* title + date */}
              <span className="absolute inset-x-0 bottom-0 p-5">
                <span className="block font-serif text-2xl font-semibold text-white">
                  {video.title}
                </span>
                <span className="mt-1 block text-sm text-white/80">{video.date}</span>
              </span>
            </button>
          </Reveal>
        ))}
      </div>

      {/* Video modal */}
      {selected && (
        <div
          className="fixed inset-0 z-[60] flex items-center justify-center bg-[oklch(0.3_0.05_250)]/85 p-4 backdrop-blur-md"
          onClick={() => setSelected(null)}
          role="dialog"
          aria-modal="true"
          aria-label={selected.title}
          style={{ animation: 'fade-up 0.4s ease-out' }}
        >
          <button
            type="button"
            aria-label="Close"
            className="glass absolute right-5 top-5 flex h-11 w-11 items-center justify-center rounded-full text-foreground"
            onClick={() => setSelected(null)}
          >
            <X className="h-5 w-5" />
          </button>

          <div
            className="glass w-full max-w-4xl overflow-hidden rounded-3xl p-3 shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="overflow-hidden rounded-2xl bg-black">
              {/* eslint-disable-next-line jsx-a11y/media-has-caption */}
              <video
                src={selected.src}
                poster={selected.thumbnail}
                controls
                autoPlay
                className="aspect-video w-full"
              />
            </div>
            <div className="p-5">
              <div className="flex flex-wrap items-baseline justify-between gap-2">
                <h3 className="font-serif text-2xl font-semibold text-foreground">
                  {selected.title}
                </h3>
                <span className="text-sm font-medium text-primary">{selected.date}</span>
              </div>
              <p className="mt-2 text-pretty leading-relaxed text-muted-foreground">
                {selected.description}
              </p>
            </div>
          </div>
        </div>
      )}
    </section>
  )
}
