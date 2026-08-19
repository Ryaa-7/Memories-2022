# Memories · UMN Angkatan 2022

Galeri kenangan dark cinematic: slideshow fullscreen (Ken Burns + fade), grid galeri hover zoom, dan video. Foto disimpan di Cloudinary, kode di GitHub.

---

## Langkah 1 — Buat akun Cloudinary (gratis)

1. Daftar di https://cloudinary.com (free tier 25 GB).
2. Masuk ke **Dashboard**. Catat 3 nilai ini:
   - `Cloud name`
   - `API Key`
   - `API Secret`

## Langkah 2 — Upload foto & video

1. Buka menu **Media Library**.
2. Buat folder baru bernama `memories`.
3. Drag-and-drop semua foto (.jpg/.png) dan video (.mp4) ke folder itu.
4. Selesai. Tidak perlu tempel URL satu per satu, app membaca folder otomatis.

> Nama folder harus sama dengan `folder` di secrets (default: `memories`).

## Langkah 3 — Jalankan di laptop dulu (opsional, untuk cek)

1. Salin `.streamlit/secrets.toml.example` menjadi `.streamlit/secrets.toml`.
2. Isi dengan kredensial dari Langkah 1.
3. Install & jalankan:
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

## Langkah 4 — Push ke GitHub

1. Buat repo baru di GitHub (boleh private).
2. Upload semua file DI PROYEK INI, KECUALI `secrets.toml` (sudah otomatis di-ignore).
   File yang masuk: `app.py`, `requirements.txt`, `.gitignore`, `README.md`, `.streamlit/secrets.toml.example`.

## Langkah 5 — Deploy ke Streamlit Cloud

1. Buka https://share.streamlit.io , login dengan GitHub.
2. Klik **New app**, pilih repo kamu, file utama `app.py`.
3. Sebelum deploy, buka **Advanced settings > Secrets**, tempel:
   ```toml
   [cloudinary]
   cloud_name = "nama_cloud_kamu"
   api_key = "1234567890"
   api_secret = "rahasia_kamu"
   folder = "memories"
   ```
4. Klik **Deploy**. Tunggu beberapa menit. Website online siap dibagikan.

---

## Menambah foto baru nanti

Cukup upload ke folder `memories` di Cloudinary. Website akan menampilkannya otomatis (cache diperbarui tiap 10 menit; restart app untuk langsung muncul).

## Catatan

- Foto dioptimasi otomatis (`f_auto,q_auto`) supaya ringan meski aslinya besar.
- Grid pakai thumbnail 1:1, klik untuk lihat versi penuh (lightbox).
- Ganti judul/subtitle di bagian `hero` dalam `app.py` bila perlu.
