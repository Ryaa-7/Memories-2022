'use client'

import { useState } from 'react'
import Image from 'next/image'
import { Gift, X, Heart, ChevronLeft, ChevronRight } from 'lucide-react'

// Daftar foto favorit. Tambah/ubah di sini.
const FAVORITES = [
  {
    src: 'https://res.cloudinary.com/e3kwzop7/image/upload/v1787128022/1678170046694.jpg',
    caption: 'Dita tidur pada saat kelas online database',
  },
  {
    src: 'https://res.cloudinary.com/e3kwzop7/image/upload/v1787142300/WhatsApp_Image_2026-08-19_at_19.20.55.jpg',
    caption: 'Lawrens Ngorok di kelas',
  },
]

export function FavoriteGift() {
  const [open, setOpen] = useState(false)
  const [i, setI] = useState(0)

  const move = (dir: number) => setI((p) => (p + dir + FAVORITES.length) % FAVORITES.length)
  const fav = FAVORITES[i]

  return (
    <>
      {/* Tombol kado mengambang */}
      <button
        onClick={() => { setI(0); setOpen(true) }}
        aria-label="Buka foto favorit"
        className="group fixed bottom-6 right-6 z-40 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-[oklch(0.72_0.11_240)] to-[oklch(0.65_0.13_275)] text-white shadow-lg shadow-[oklch(0.6_0.12_255)]/40 transition-transform duration-300 hover:scale-110 animate-wiggle"
      >
        <Gift className="h-7 w-7" />
        <span className="pointer-events-none absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-white/70" />
          <span className="relative inline-flex h-2.5 w-2.5 rounded-full bg-white" />
        </span>
      </button>

      {/* Pop up foto favorit */}
      {open && (
        <div
          onClick={() => setOpen(false)}
          className="fixed inset-0 z-50 flex items-center justify-center bg-[oklch(0.6_0.08_245)]/50 p-5 backdrop-blur-md animate-fade-in"
        >
          <div
            onClick={(e) => e.stopPropagation()}
            className="relative w-full max-w-md overflow-hidden rounded-3xl border-4 border-white bg-white shadow-2xl animate-pop"
          >
            <button
              onClick={() => setOpen(false)}
              aria-label="Tutup"
              className="absolute right-3 top-3 z-10 flex h-9 w-9 items-center justify-center rounded-full bg-white/90 text-[oklch(0.5_0.1_255)] shadow transition-transform hover:rotate-90"
            >
              <X className="h-5 w-5" />
            </button>

            <div className="relative aspect-[3/4] w-full bg-[oklch(0.92_0.03_240)]">
              <Image
                key={fav.src}
                src={fav.src}
                alt={fav.caption}
                fill
                unoptimized
                className="object-cover animate-fade-in"
              />

              {/* Navigasi geser (muncul jika lebih dari 1 foto) */}
              {FAVORITES.length > 1 && (
                <>
                  <button
                    onClick={() => move(-1)}
                    aria-label="Sebelumnya"
                    className="absolute left-2 top-1/2 flex h-10 w-10 -translate-y-1/2 items-center justify-center rounded-full bg-white/80 text-[oklch(0.5_0.1_255)] shadow transition hover:bg-white hover:scale-110"
                  >
                    <ChevronLeft className="h-5 w-5" />
                  </button>
                  <button
                    onClick={() => move(1)}
                    aria-label="Berikutnya"
                    className="absolute right-2 top-1/2 flex h-10 w-10 -translate-y-1/2 items-center justify-center rounded-full bg-white/80 text-[oklch(0.5_0.1_255)] shadow transition hover:bg-white hover:scale-110"
                  >
                    <ChevronRight className="h-5 w-5" />
                  </button>
                </>
              )}
            </div>

            <div className="flex items-start gap-2 p-5">
              <Heart className="mt-1 h-5 w-5 shrink-0 fill-[oklch(0.7_0.17_15)] text-[oklch(0.7_0.17_15)]" />
              <div className="flex-1">
                <p className="font-sans text-xs font-semibold uppercase tracking-[0.2em] text-primary">
                  Foto Terfavorit{FAVORITES.length > 1 ? ` · ${i + 1}/${FAVORITES.length}` : ''}
                </p>
                <p className="mt-1 font-serif text-lg leading-snug text-foreground">
                  {fav.caption}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
