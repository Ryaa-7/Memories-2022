'use client'

import { Heart, Camera, AtSign, Send, ArrowUp } from 'lucide-react'

const socials = [
  { label: 'Photo journal', icon: Camera, href: '#' },
  { label: 'Reach out', icon: AtSign, href: '#' },
  { label: 'Share', icon: Send, href: '#' },
]

export function Footer() {
  return (
    <footer className="relative mx-auto max-w-6xl px-5 pb-12 pt-10 text-center">
      <div className="glass rounded-[2rem] px-6 py-12 shadow-lg shadow-[oklch(0.72_0.11_240)]/10">
        <Heart className="mx-auto h-8 w-8 animate-float-slow fill-primary text-primary" />
        <p className="mx-auto mt-5 max-w-md text-balance font-serif text-2xl font-medium leading-snug text-foreground md:text-3xl">
          Made with CAPEK njir, for the memories we&apos;ll never forget.
        </p>

        <div className="mt-7 flex justify-center gap-3">
          {socials.map((s) => (
            <a
              key={s.label}
              href={s.href}
              aria-label={s.label}
              className="flex h-11 w-11 items-center justify-center rounded-full bg-primary/10 text-foreground/80 transition-all hover:scale-110 hover:bg-primary hover:text-primary-foreground"
            >
              <s.icon className="h-5 w-5" />
            </a>
          ))}
        </div>

        <a
          href="#home"
          className="mt-8 inline-flex items-center gap-2 rounded-full px-5 py-2.5 text-sm font-medium text-primary transition-colors hover:bg-primary/10"
        >
          <ArrowUp className="h-4 w-4" />
          Back to top
        </a>

        <p className="mt-8 text-xs text-muted-foreground">
          © {new Date().getFullYear()} Our Memories. Every moment, kept close.
        </p>
      </div>
    </footer>
  )
}
