export type Category =
  | 'Favorite'
  | 'Moments'
  | 'Adventures'
  | 'Celebrations'
  | 'Random'

export interface Photo {
  id: string
  src: string
  caption: string
  category: Category
  span: 'tall' | 'wide' | 'normal'
}

export const categories: ('All' | Category)[] = [
  'All',
  'Favorite',
  'Moments',
  'Adventures',
  'Celebrations',
  'Random',
]

export const photos: Photo[] = [
  {
    id: 'p1',
    src: '/memories/photo-1.png',
    caption: 'Fields where we got lost together',
    category: 'Adventures',
    span: 'tall',
  },
  {
    id: 'p2',
    src: '/memories/photo-2.png',
    caption: 'Slow mornings and warm coffee',
    category: 'Moments',
    span: 'wide',
  },
  {
    id: 'p3',
    src: '/memories/photo-3.png',
    caption: 'The lake that held our reflection',
    category: 'Adventures',
    span: 'normal',
  },
  {
    id: 'p4',
    src: '/memories/photo-4.png',
    caption: 'Another year, another wish',
    category: 'Celebrations',
    span: 'tall',
  },
  {
    id: 'p5',
    src: '/memories/photo-5.png',
    caption: 'Watching the world go by',
    category: 'Random',
    span: 'wide',
  },
  {
    id: 'p6',
    src: '/memories/photo-6.png',
    caption: 'First snow, endless laughter',
    category: 'Favorite',
    span: 'normal',
  },
  {
    id: 'p7',
    src: '/memories/photo-7.png',
    caption: 'A quiet afternoon by the water',
    category: 'Moments',
    span: 'wide',
  },
  {
    id: 'p8',
    src: '/memories/photo-8.png',
    caption: 'Counting stars until we forgot the time',
    category: 'Favorite',
    span: 'tall',
  },
]

export interface Video {
  id: string
  thumbnail: string
  title: string
  date: string
  duration: string
  description: string
  src: string
}

export const videos: Video[] = [
  {
    id: 'v1',
    thumbnail: '/memories/video-1.png',
    title: 'A Day to Remember',
    date: 'June 2024',
    duration: '2:14',
    description:
      'The morning we watched the sun rise over the hills and promised to remember every second of it.',
    src: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
  },
  {
    id: 'v2',
    thumbnail: '/memories/video-2.png',
    title: 'Our Little Adventure',
    date: 'August 2024',
    duration: '3:48',
    description:
      'A spontaneous road trip toward the mountains, windows down, playlist loud, hearts wide open.',
    src: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
  },
  {
    id: 'v3',
    thumbnail: '/memories/video-3.png',
    title: 'Moments We Keep',
    date: 'November 2024',
    duration: '1:57',
    description:
      'Quiet pages, soft light, and all the little things we never wanted to let slip away.',
    src: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
  },
  {
    id: 'v4',
    thumbnail: '/memories/video-4.png',
    title: 'The Best Days',
    date: 'February 2025',
    duration: '4:22',
    description:
      'Bonfires and blue twilight with the people who make everything feel like home.',
    src: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4',
  },
]

export interface TimelineEntry {
  year: string
  title: string
  description: string
}

export const timeline: TimelineEntry[] = [
  {
    year: '2022',
    title: 'Where It All Started',
    description: 'The first hello that quietly changed everything.',
  },
  {
    year: '2023',
    title: 'TURU',
    description: 'A year of small joys we learned to treasure.',
  },
  {
    year: '2024',
    title: 'NGOBOK',
    description: 'New places, new stories, the same wonderful company.',
  },
  {
    year: '2025',
    title: 'TURU',
    description: 'The days we will tell stories about for years.',
  },
  {
    year: '2026',
    title: 'LULUS ANJAY!!!',
    description: 'And the story is only just beginning.',
  },
]
