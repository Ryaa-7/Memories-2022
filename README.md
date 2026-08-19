# Memories · UMN Angkatan 2022 (Next.js)

Galeri kenangan soft-blue: hero parallax, featured memory, galeri masonry, timeline, dan video. Foto & video ditarik otomatis dari Cloudinary. Deploy ke Vercel.

---

## Cara kerja singkat

Kode ambil foto/video dari folder Cloudinary lewat API route `/api/memories` (aman di server, API Secret tidak bocor ke browser). Kamu tidak perlu menempel URL foto satu per satu. Tambah foto baru = upload ke folder Cloudinary, muncul otomatis.

## Langkah 1 — Push ke GitHub

1. Buat repo baru di GitHub (boleh private).
2. Upload SEMUA isi folder ini KECUALI `node_modules` dan `.next` (sudah otomatis di-ignore).
   Jangan upload file `.env.local` kalau ada.

## Langkah 2 — Deploy ke Vercel

1. Buka https://vercel.com , login pakai GitHub (gratis).
2. Klik **Add New > Project**, pilih repo tadi, klik **Import**.
3. Vercel otomatis mengenali Next.js. JANGAN klik Deploy dulu.
4. Buka bagian **Environment Variables**, tambahkan 4 ini (nilai dari Dashboard Cloudinary):

   | Name | Value |
   |------|-------|
   | `CLOUDINARY_CLOUD_NAME` | nama cloud kamu (mis. `e3kwzop7`) |
   | `CLOUDINARY_API_KEY` | API Key kamu |
   | `CLOUDINARY_API_SECRET` | API Secret kamu |
   | `CLOUDINARY_FOLDER` | `memories` |

5. Klik **Deploy**. Tunggu beberapa menit. Vercel kasih link publik (mis. `namaproyek.vercel.app`).

## Menambah foto/video baru nanti

Upload ke folder `memories` di Cloudinary. Muncul otomatis (cache 5 menit; buka lagi setelah itu, atau redeploy dari dashboard Vercel untuk langsung).

## Tes di laptop (opsional)

```bash
npm install
cp .env.example .env.local   # lalu isi kredensial
npm run dev
```
Buka http://localhost:3000

## Catatan

- Foto dioptimasi otomatis (`f_auto,q_auto`) supaya ringan.
- Thumbnail video diambil dari frame pertama otomatis.
- Judul, subtitle, dan teks timeline bisa diubah di `lib/memories-data.ts` (bagian timeline) dan komponen di `components/`.
- Kalau galeri kosong padahal foto ada: cek 4 Environment Variables di Vercel sudah benar dan `CLOUDINARY_CLOUD_NAME` sama persis dengan cloud tempat upload.
