'use client'

import { timeline } from '@/lib/memories-data'
import { Reveal } from '@/components/reveal'
import { cn } from '@/lib/utils'

export function Timeline() {
  return (
    <section id="timeline" className="relative mx-auto max-w-4xl scroll-mt-24 px-5 py-24">
      <Reveal className="mb-16 text-center">
        <p className="font-sans text-sm font-medium uppercase tracking-[0.3em] text-primary">
          Through The Years
        </p>
        <h2 className="mt-3 text-balance font-serif text-4xl font-semibold text-foreground md:text-5xl">
          Our Memory Timeline
        </h2>
      </Reveal>

      <div className="relative">
        {/* glowing line */}
        <div className="absolute left-4 top-0 h-full w-px bg-gradient-to-b from-primary/10 via-primary/60 to-primary/10 md:left-1/2 md:-translate-x-1/2">
          <div className="absolute inset-0 blur-sm" />
        </div>

        <ul className="space-y-12">
          {timeline.map((entry, i) => {
            const left = i % 2 === 0
            return (
              <Reveal
                as="li"
                key={entry.year}
                delay={i * 80}
                className={cn(
                  'relative flex md:items-center',
                  left ? 'md:flex-row' : 'md:flex-row-reverse',
                )}
              >
                {/* dot */}
                <span className="absolute left-4 top-2 z-10 flex h-4 w-4 -translate-x-1/2 items-center justify-center md:left-1/2">
                  <span className="absolute h-4 w-4 animate-ping rounded-full bg-primary/40" />
                  <span className="h-3 w-3 rounded-full bg-primary shadow-md shadow-primary/50 ring-4 ring-background" />
                </span>

                <div className="w-full pl-10 md:w-1/2 md:pl-0">
                  <div
                    className={cn(
                      'glass rounded-3xl p-6 shadow-lg shadow-[oklch(0.72_0.11_240)]/10 transition-transform hover:scale-[1.02]',
                      left ? 'md:mr-10' : 'md:ml-10',
                    )}
                  >
                    <span className="font-serif text-3xl font-semibold text-primary">
                      {entry.year}
                    </span>
                    <h3 className="mt-1 font-serif text-xl font-medium text-foreground">
                      {entry.title}
                    </h3>
                    <p className="mt-2 text-pretty text-sm leading-relaxed text-muted-foreground">
                      {entry.description}
                    </p>
                  </div>
                </div>
              </Reveal>
            )
          })}
        </ul>
      </div>
    </section>
  )
}
