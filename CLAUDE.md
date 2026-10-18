# MAKA Project — Website Foto Wisuda

Landing page satu halaman untuk **MAKA Project**, jasa foto wisuda di Malang, Jawa Timur.
Semua teks berbahasa Indonesia dengan nada santai dan hangat ("kamu", "kami", "chat dulu aja").

## Tujuan website

- Meyakinkan calon wisudawan bahwa mereka **tidak perlu jago pose** karena semua pose diarahkan dari awal sampai akhir sesi.
- Menonjolkan foto bersama keluarga dan orang tersayang, hasil edit dalam **4–5 hari kerja**, dan **semua file original (JPEG)** yang selalu termasuk.
- Konversi utama: tombol **"Check Jadwal"** (membuka Google Spreadsheet jadwal) dan **chat WhatsApp**. Pesannya "ngobrol dulu, booking belakangan" — chat tidak mengikat.
- Tagline: *"Toga dipakai sekali. Ceritanya selamanya."* Judul hero: *"Cerita Selamanya."*

## Teknologi

- Satu file `index.html` (~1.400 baris) berisi HTML, CSS (`<style>`), dan JS vanilla (`<script>`). Tidak ada framework, bundler, atau npm.
- Font dimuat dari Google Fonts. Tidak ada library JS eksternal.
- Aset dihasilkan oleh `tools/build_assets.py` (Python + Pillow + NumPy).

## Gaya desain

- Nuansa **editorial, gelap, dan sinematik**: latar hitam hangat, teks krem, aksen judul memakai *italic serif* (`<em>`).
- Section **Paket** sengaja dibuat terang (tema krem, `data-light` / `.content.light`) sebagai kontras.
- Animasi: splash loading berisi logo dan progress bar, **bola 3D berisi 21 foto** di hero (bisa diseret dan berputar), smooth scroll dengan wheel, teks manifesto muncul kata per kata, parallax foto, reveal saat elemen masuk layar, strip foto yang berjalan sendiri, dan kursor titik kustom (hanya di desktop).
- Menghormati `prefers-reduced-motion`, safe-area iPhone (`env(safe-area-inset-*)`), dan ukuran tap minimal 44px.
- Tone foto adalah ciri khas MAKA (hangat keemasan) dan **tidak menerima request tone lain**. Ini juga disebut di FAQ.

## Warna (CSS variables di `:root`)

| Token | Nilai | Pemakaian |
|---|---|---|
| `--bg` | `#121110` | Latar utama (gelap) dan `theme-color` |
| `--ink` | `#efebe4` | Teks utama (krem) |
| `--dim` | `#8f8a82` | Teks sekunder |
| `--line` | `rgba(239,235,228,.16)` | Garis dan border |
| `--cream` | `#ece7de` | Latar section terang (Paket) |
| `--char` | `#1b1a18` | Teks di section terang dan kartu paket unggulan |

Tema terang: `--bg:#ece7de; --ink:#1b1a18; --dim:#6f6960`.
Warna logo di `build_assets.py`: CREAM `(239,235,228)`, INK `(24,23,21)`.

## Font

- **Playfair Display** (400, 500, italic 400) untuk judul dan aksen serif → `--serif`
- **Inter** (300, 400, 500) untuk teks isi dan UI → `--sans`

## Struktur halaman

1. **Splash**: logo, progress bar (menunggu 21 foto bola selesai dimuat, maksimal 6,5 detik), dan teks "Foto Wisuda · Malang".
2. **Header**: wordmark "Maka *Project*", tombol "Check Jadwal", dan tombol Menu.
3. **Hero**: bola 3D foto, judul "Cerita Selamanya.", dan teks bio. Tombol grid membuka **Arsip karya** (semua foto). Klik foto membuka **lightbox** (bisa pakai panah kiri/kanan dan swipe).
4. `#cerita` **01 — Kenapa difoto**: manifesto.
5. `#rasa` **02 — Yang kami jaga**: tiga keunggulan (tidak perlu jago pose, foto bersama keluarga, hasil cepat + file original JPEG).
6. **Strip**: semua foto dalam satu baris yang bergeser otomatis dan bisa digeser manual.
7. `#alur` **03 — Cara kerjanya**: Chat dulu → Kunci jadwal → Datang & nikmati.
8. `#paket` **04 — Paket** (tema krem).
9. `#tanya` **05 — Pertanyaan**: FAQ accordion.
10. `#kontak` **06 — Chat dulu aja**: WhatsApp dan Instagram.
11. **Footer** dan **dock "Check Jadwal"** yang menempel di bawah layar pada mobile.

## Data bisnis (diubah di objek JS, bukan di HTML)

Blok `/* GANTI DATA DI SINI */` di `<script>`:

- `CFG.whatsapp`: `6285925568532` (format 62…, ditampilkan sebagai 0859-2556-8532)
- `CFG.instagram` / `instagramHandle`: `@makaproject._`
- `CFG.scheduleSheet`: link Google Spreadsheet jadwal. Kalau dikosongkan, tombol "Check Jadwal" mengarah ke WhatsApp atau `#kontak`.
- `CFG.packagePhotos`: `false`, artinya kartu paket tanpa foto. Bisa dites dengan `?paketfoto=1`.

Array data lainnya:

- `PACKAGES`:
  - **Sesi 1 Jam**: Rp 200.000, 15 foto edit + semua file original (JPEG).
  - **Sesi 2 Jam** (unggulan, `hi: true`): Rp 270.000, 25 foto edit + semua file original (JPEG).
  - **Extend**: Rp 50.000 / 20 menit, berlaku untuk kedua paket.
- `FAQ`: 6 pertanyaan.
- `PHOTOS`: daftar `[kode, rasio]`. **Harus sama dengan** `assets/photo/manifest.json`.
- `SPHERE`: 21 indeks foto untuk bola hero. Indeks 41 & 42 adalah foto Okt 2026 yang menggantikan dua foto Gracia.
- `STRIP`: urutan strip. Foto baru diselipkan setiap 4 foto lama.

⚠️ Teks yang di-hardcode di HTML dan harus ikut diperbarui kalau harga berubah:
- "Selisihnya cuma **Rp 70.000**…" (`.pk-note`)
- "Extend Rp 50.000 / 20 menit" (di section Paket dan di FAQ)

## Struktur folder

```
Web MAKA/
├─ index.html            # seluruh website
├─ Logo.png              # logo sumber (dibersihkan otomatis jadi PNG transparan)
├─ .gitignore            # mengecualikan Porto/
├─ Porto/                # foto ASLI resolusi penuh (~340 MB) — sumber saja, tidak masuk git; website tidak memuat apa pun dari sini
├─ assets/
│  ├─ brand/             # mark-cream.png, mark-ink.png, favicon.png, og.jpg (1200×630, dari foto p06)
│  └─ photo/             # pNN-s.webp (720px), -m (1280px), -l (2000px) + manifest.json
└─ tools/
   └─ build_assets.py    # generator aset brand + foto
```

## Alur menambah atau mengganti foto

1. Taruh file di `Porto/`.
2. Tambahkan nama filenya ke list `ORDER` di `tools/build_assets.py`. Script akan error kalau ada foto di Porto yang belum masuk `ORDER`. 21 foto pertama adalah foto bola hero bawaan.
3. Jalankan `python tools/build_assets.py` dari folder Web MAKA. Foto yang sudah punya file webp dilewati, kecuali p06 yang selalu dibuat ulang untuk `og.jpg`.
4. Salin isi `assets/photo/manifest.json` ke `PHOTOS` di `index.html`. Kalau perlu, sesuaikan `SPHERE`, `STRIP`, dan `data-photo="N"` di section (indeksnya mulai dari 0).

Keputusan sebelumnya: **semua foto di Porto ditampilkan** (permintaan 10 Okt 2026, `SKIP` kosong). Sekarang ada 46 foto, termasuk tambahan 18 Okt 2026 (p39–p46).

## Belum selesai / perlu dicek

- **Belum di-hosting.** Belum ada domain, belum ada git, dan belum ada konfigurasi deploy. Saat deploy, keluarkan folder `Porto/` dan `tools/`.
- `og:image` masih berupa path relatif (`assets/brand/og.jpg`). Supaya preview muncul di WhatsApp dan media sosial, path ini harus jadi URL absolut setelah domain ada. Tambahkan juga `og:url` dan `canonical`.
- Belum ada SEO lokal lanjutan: structured data (LocalBusiness), `sitemap.xml`, dan `robots.txt`.
- Belum ada analytics atau pelacakan klik tombol WhatsApp / Check Jadwal.
- Tombol "Hubungi" di kartu paket hanya scroll ke `#kontak`. Tombol ini belum membuka WhatsApp dengan pesan yang menyebut nama paket.
- Foto di kartu paket (`packagePhotos`) belum diputuskan. Default saat ini tanpa foto.
- Hitungan lightbox di HTML masih tertulis `/ 33` (sisa versi lama). Angkanya dikoreksi otomatis oleh JS saat lightbox dibuka, jadi ini hanya kosmetik.
- Spreadsheet jadwal harus disetel "siapa saja yang memiliki link dapat melihat".
