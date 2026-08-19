'use client'

import { useMemo, useState } from 'react'
import Image from 'next/image'
import { Heart, X, ChevronLeft, ChevronRight } from 'lucide-react'
import { cn } from '@/lib/utils'
import { categories, type Photo } from '@/lib/memories-data'
import { useMemories } from '@/lib/use-memories'
import { Reveal } from '@/components/reveal'

export function MemoryGallery() {
  const { photos, loading } = useMemories()
  const [active, setActive] = useState<(typeof categories)[number]>('All')
  const [favorites, setFavorites] = useState<Record<string, boolean>>({})
  const [lightbox, setLightbox] = useState<number | null>(null)

  const filtered = useMemo(() => {
    if (active === 'All') return photos
    if (active === 'Favorite')
      return photos.filter((p) => p.category === 'Favorite' || favorites[p.id])
    return photos.filter((p) => p.category === active)
  }, [active, favorites, photos])

  const toggleFav = (id: string) =>
    setFavorites((f) => ({ ...f, [id]: !f[id] }))

  const openAt = (photo: Photo) => {
    const idx = filtered.findIndex((p) => p.id === photo.id)
    setLightbox(idx)
  }

  const step = (dir: number) => {
    setLightbox((cur) => {
      if (cur === null) return cur
      return (cur + dir + filtered.length) % filtered.length
    })
  }

  const spanClass = (span: Photo['span']) =>
    span === 'tall'
      ? 'row-span-2'
      : span === 'wide'
        ? 'sm:col-span-2'
        : ''

  return (
    <section id="memories" className="relative mx-auto max-w-6xl scroll-mt-24 px-5 py-24">
      <Reveal className="mb-4 text-center">
        <p className="font-sans text-sm font-medium uppercase tracking-[0.3em] text-primary">
          The Gallery
        </p>
        <h2 className="mt-3 text-balance font-serif text-4xl font-semibold text-foreground md:text-5xl">
          A collection of little moments
        </h2>
        <p className="mx-auto mt-4 max-w-lg text-pretty leading-relaxed text-muted-foreground">
          Every photo is a feeling we get to keep. Wander through, linger a while,
          and let the memories find you.
        </p>
      </Reveal>

      {/* category filter (disembunyikan: foto dari Cloudinary tanpa kategori) */}
      <div
        id="photos"
        className="mb-10 mt-10 hidden snap-x gap-2 overflow-x-auto scroll-mt-28 pb-2 [scrollbar-width:none] md:flex-wrap md:justify-center md:overflow-visible"
      >
        {categories.map((cat) => (
          <button
            key={cat}
            type="button"
            onClick={() => setActive(cat)}
            className={cn(
              'shrink-0 snap-start rounded-full px-5 py-2 text-sm font-medium transition-all',
              active === cat
                ? 'bg-primary text-primary-foreground shadow-md shadow-primary/30'
                : 'glass text-muted-foreground hover:text-foreground',
            )}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* masonry-ish grid */}
      <div className="grid auto-rows-[220px] grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">
        {filtered.map((photo, i) => (
          <Reveal
            key={photo.id}
            delay={i * 60}
            className={cn('group relative', spanClass(photo.span))}
          >
            <button
              type="button"
              onClick={() => openAt(photo)}
              className="relative block h-full w-full overflow-hidden rounded-3xl shadow-md shadow-[oklch(0.72_0.11_240)]/10 outline-none ring-primary/50 transition-all duration-500 hover:shadow-2xl hover:shadow-primary/30 focus-visible:ring-2"
            >
              <Image
                src={photo.src}
                alt={photo.caption}
                fill
                sizes="(max-width: 768px) 50vw, 25vw"
                className="object-cover transition-transform duration-700 ease-out group-hover:scale-110"
              />
              {/* glow ring */}
              <span className="pointer-events-none absolute inset-0 rounded-3xl ring-1 ring-inset ring-white/30" />
              {/* caption overlay */}
              {photo.caption && (
                <span className="absolute inset-x-0 bottom-0 translate-y-3 bg-gradient-to-t from-[oklch(0.4_0.06_250)]/85 to-transparent p-4 text-left opacity-0 transition-all duration-500 group-hover:translate-y-0 group-hover:opacity-100">
                  <span className="text-pretty font-serif text-base font-medium leading-snug text-white">
                    {photo.caption}
                  </span>
                </span>
              )}
            </button>

            <button
              type="button"
              onClick={() => toggleFav(photo.id)}
              aria-label={favorites[photo.id] ? 'Remove favorite' : 'Add to favorites'}
              className="glass absolute right-3 top-3 flex h-9 w-9 items-center justify-center rounded-full"
            >
              <Heart
                className={cn(
                  'h-4 w-4 transition-colors',
                  favorites[photo.id]
                    ? 'animate-heart-pop fill-rose-400 text-rose-400'
                    : 'text-foreground/70',
                )}
              />
            </button>
          </Reveal>
        ))}
      </div>

      {filtered.length === 0 && (
        <div className="glass mx-auto mt-6 max-w-md rounded-3xl p-10 text-center">
          <Heart className="mx-auto mb-3 h-8 w-8 text-primary/60" />
          <p className="font-serif text-xl text-foreground">No memories here yet</p>
          <p className="mt-2 text-sm text-muted-foreground">
            Tap the heart on a photo to start your favorites.
          </p>
        </div>
      )}

      {/* Lightbox */}
      {lightbox !== null && filtered[lightbox] && (
        <div
          className="fixed inset-0 z-[60] flex items-center justify-center bg-[oklch(0.3_0.05_250)]/80 p-4 backdrop-blur-md"
          onClick={() => setLightbox(null)}
          role="dialog"
          aria-modal="true"
          aria-label={filtered[lightbox].caption}
          style={{ animation: 'fade-up 0.4s ease-out' }}
        >
          <button
            type="button"
            aria-label="Close"
            className="glass absolute right-5 top-5 flex h-11 w-11 items-center justify-center rounded-full text-foreground"
            onClick={() => setLightbox(null)}
          >
            <X className="h-5 w-5" />
          </button>

          <button
            type="button"
            aria-label="Previous"
            className="glass absolute left-4 top-1/2 flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full text-foreground md:left-8"
            onClick={(e) => {
              e.stopPropagation()
              step(-1)
            }}
          >
            <ChevronLeft className="h-5 w-5" />
          </button>

          <button
            type="button"
            aria-label="Next"
            className="glass absolute right-4 top-1/2 flex h-11 w-11 -translate-y-1/2 items-center justify-center rounded-full text-foreground md:right-8"
            onClick={(e) => {
              e.stopPropagation()
              step(1)
            }}
          >
            <ChevronRight className="h-5 w-5" />
          </button>

          <figure
            className="relative flex max-h-[85vh] w-full max-w-4xl flex-col items-center"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="relative h-[70vh] w-full overflow-hidden rounded-3xl shadow-2xl">
              <Image
                src={filtered[lightbox].src}
                alt={filtered[lightbox].caption}
                fill
                className="object-contain"
              />
            </div>
            {filtered[lightbox].caption && (
              <figcaption className="mt-5 text-center font-serif text-xl text-white text-glow">
                {filtered[lightbox].caption}
              </figcaption>
            )}
          </figure>
        </div>
      )}
    </section>
  )
}
