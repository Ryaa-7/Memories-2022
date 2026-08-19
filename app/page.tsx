import { AmbientBackground } from '@/components/ambient-background'
import { Navbar } from '@/components/navbar'
import { Hero } from '@/components/hero'
import { MemoryGallery } from '@/components/memory-gallery'
import { VideoSection } from '@/components/video-section'
import { Timeline } from '@/components/timeline'
import { FeaturedMemory } from '@/components/featured-memory'
import { Footer } from '@/components/footer'

export default function Page() {
  return (
    <>
      <AmbientBackground />
      <Navbar />
      <main className="relative">
        <Hero />
        <MemoryGallery />
        <VideoSection />
        <Timeline />
        <FeaturedMemory />
        <Footer />
      </main>
    </>
  )
}
