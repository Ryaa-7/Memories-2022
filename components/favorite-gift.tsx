'use client'

import { useState } from 'react'
import Image from 'next/image'
import { Gift, X, Heart } from 'lucide-react'

const FAVORITE_SRC =
  'https://res.cloudinary.com/e3kwzop7/image/upload/v1787128022/1678170046694.jpg'
const FAVORITE_CAPTION = 'Dita tidur pada saat kelas online database'

export function FavoriteGift() {
  const [open, setOpen] = useState(false)

  return (
    <>
      {/* Tombol kado mengambang */}
      <button
        onClick={() => setOpen(true)}
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
                src={FAVORITE_SRC}
                alt={FAVORITE_CAPTION}
                fill
                unoptimized
                className="object-cover"
              />
            </div>

            <div className="flex items-start gap-2 p-5">
              <Heart className="mt-1 h-5 w-5 shrink-0 fill-[oklch(0.7_0.17_15)] text-[oklch(0.7_0.17_15)]" />
              <div>
                <p className="font-sans text-xs font-semibold uppercase tracking-[0.2em] text-primary">
                  Foto Terfavorit
                </p>
                <p className="mt-1 font-serif text-lg leading-snug text-foreground">
                  {FAVORITE_CAPTION}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
