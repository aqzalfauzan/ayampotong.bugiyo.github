# Ayam Potong Bu Giyo — blog

Blog statis (HTML + CSS, tanpa build) berisi catatan seputar usaha ayam potong di Lampung.
Siap di-hosting gratis lewat **GitHub Pages**.

## Isi situs

| File | Fungsi |
| --- | --- |
| `index.html` | Beranda: daftar artikel, pencarian, label, arsip, sidebar |
| `artikel/bisnis-ayam-potong-lampung-2026.html` | Halaman artikel (daftar isi, tombol bagikan, kotak penulis) |
| `tentang.html` | Halaman tentang blog |
| `404.html` | Halaman "tidak ditemukan" |
| `feed.xml` | RSS untuk pembaca feed |
| `sitemap.xml`, `robots.txt` | Untuk Google Search Console |
| `artikel-ayam-potong-lampung.html` | Alamat lama, otomatis dialihkan ke alamat artikel baru |
| `assets/` | CSS, JavaScript, favicon, dan gambar sampul |

## Menayangkan situs

Situs memakai domain sendiri **https://aratikel.blog/** (lihat file `CNAME`).

1. Gabungkan (merge) perubahan ke `main`.
2. Di GitHub buka **Settings → Pages**, pilih **Source: Deploy from a branch**, branch **`main`**, folder **`/ (root)`**, lalu **Save**.
3. Di pengaturan DNS domain `aratikel.blog` (di registrar tempat membeli domain), isi:
   - 4 record **A** untuk `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - 1 record **CNAME** untuk `www` → `aqzalfauzan.github.io`
4. Kembali ke **Settings → Pages**, tunggu sampai muncul "DNS check successful", lalu centang **Enforce HTTPS**. Domain `.blog` hanya bisa dibuka lewat HTTPS.

Semua alamat lengkap (canonical, pratinjau tautan, RSS, sitemap) sudah memakai `https://aratikel.blog/`. Jika domain berganti, cari-dan-ganti alamat itu di file HTML, `feed.xml`, `sitemap.xml`, `robots.txt`, dan ubah isi `CNAME`.

## Menambah artikel baru

1. Salin `artikel/bisnis-ayam-potong-lampung-2026.html` menjadi file baru di folder `artikel/`, lalu ganti judul, deskripsi, tanggal, label, dan isinya.
2. Tambahkan kartu artikel baru di `index.html` (di dalam `data-post-list`, di atas artikel lama) dan perbarui widget **Artikel terbaru**, **Label**, dan **Arsip** di sidebar.
3. Tambahkan `<item>` baru di `feed.xml` dan `<url>` baru di `sitemap.xml`.
4. Opsional: buat gambar sampul 1200×630 piksel di `assets/img/` untuk pratinjau WhatsApp/Facebook.
