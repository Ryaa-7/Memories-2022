'use client'

import { useEffect, useState } from 'react'
import type { Photo } from '@/lib/memories-data'
import type { Video } from '@/lib/memories-data'

export interface MemoriesData {
  photos: Photo[]
  videos: Video[]
  loading: boolean
  error: string | null
}

let cache: { photos: Photo[]; videos: Video[] } | null = null

export function useMemories(): MemoriesData {
  const [photos, setPhotos] = useState<Photo[]>(cache?.photos ?? [])
  const [videos, setVideos] = useState<Video[]>(cache?.videos ?? [])
  const [loading, setLoading] = useState(!cache)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (cache) return
    let alive = true
    fetch('/api/memories')
      .then((r) => r.json())
      .then((d) => {
        if (!alive) return
        if (d.error) setError(d.error)
        const p = (d.photos ?? []) as Photo[]
        const v = (d.videos ?? []) as Video[]
        cache = { photos: p, videos: v }
        setPhotos(p)
        setVideos(v)
      })
      .catch((e) => alive && setError(String(e)))
      .finally(() => alive && setLoading(false))
    return () => {
      alive = false
    }
  }, [])

  return { photos, videos, loading, error }
}
