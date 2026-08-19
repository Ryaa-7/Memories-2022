import { NextResponse } from 'next/server'
import { v2 as cloudinary } from 'cloudinary'

// Konfigurasi dari environment variables (aman, tidak terekspos ke browser)
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET,
  secure: true,
})

const FOLDER = process.env.CLOUDINARY_FOLDER || 'memories'

// cache 5 menit di sisi server
export const revalidate = 300

type Item = { public_id: string; asset_folder: string; secure_url: string; width: number; height: number }

async function pull(resourceType: 'image' | 'video'): Promise<Item[]> {
  const items: Item[] = []
  let cursor: string | undefined = undefined
  do {
    const res: any = await cloudinary.api.resources({
      type: 'upload',
      resource_type: resourceType,
      max_results: 500,
      next_cursor: cursor,
    })
    for (const r of res.resources || []) {
      items.push({
        public_id: r.public_id || '',
        asset_folder: r.asset_folder || r.folder || '',
        secure_url: r.secure_url || '',
        width: r.width || 0,
        height: r.height || 0,
      })
    }
    cursor = res.next_cursor
  } while (cursor)
  return items
}

function inTarget(it: Item, folder: string) {
  const f = folder.replace(/^\/+|\/+$/g, '').toLowerCase()
  return (
    (it.asset_folder || '').replace(/^\/+|\/+$/g, '').toLowerCase().startsWith(f) ||
    (it.public_id || '').toLowerCase().startsWith(f + '/')
  )
}
function notSample(it: Item) {
  return !(
    (it.public_id || '').toLowerCase().startsWith('samples/') ||
    (it.asset_folder || '').toLowerCase() === 'samples'
  )
}

// tebak span masonry dari rasio (tall / wide / normal) agar layout hidup
function spanOf(w: number, h: number): 'tall' | 'wide' | 'normal' {
  if (!w || !h) return 'normal'
  const r = w / h
  if (r < 0.8) return 'tall'
  if (r > 1.5) return 'wide'
  return 'normal'
}

function opt(url: string, w = 1200) {
  return url.includes('/upload/')
    ? url.replace('/upload/', `/upload/f_auto,q_auto,w_${w}/`)
    : url
}

export async function GET() {
  try {
    if (
      !process.env.CLOUDINARY_CLOUD_NAME ||
      !process.env.CLOUDINARY_API_KEY ||
      !process.env.CLOUDINARY_API_SECRET
    ) {
      return NextResponse.json(
        { error: 'Cloudinary env belum diset', photos: [], videos: [] },
        { status: 200 },
      )
    }

    const [allImg, allVid] = [await pull('image'), await pull('video')]

    let imgs = allImg.filter((it) => inTarget(it, FOLDER))
    let vids = allVid.filter((it) => inTarget(it, FOLDER))
    if (imgs.length === 0 && vids.length === 0) {
      imgs = allImg.filter(notSample)
      vids = allVid.filter(notSample)
    }

    const photos = imgs.map((it, i) => ({
      id: it.public_id || `p${i}`,
      src: opt(it.secure_url, 1200),
      caption: '',
      category: 'Moments' as const,
      span: spanOf(it.width, it.height),
    }))

    const videos = vids.map((it, i) => ({
      id: it.public_id || `v${i}`,
      title: `Video ${i + 1}`,
      date: '',
      duration: '',
      description: '',
      thumbnail: it.secure_url.replace('/upload/', '/upload/so_0,f_jpg,w_1200/').replace(/\.[^/.]+$/, '.jpg'),
      src: it.secure_url,
    }))

    return NextResponse.json({ photos, videos })
  } catch (e: any) {
    return NextResponse.json(
      { error: String(e?.message || e), photos: [], videos: [] },
      { status: 200 },
    )
  }
}
