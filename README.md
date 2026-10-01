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

## Menayangkan situs (gratis)

1. Gabungkan (merge) branch ini ke `main`.
2. Di GitHub buka **Settings → Pages**.
3. Pada **Build and deployment**, pilih **Source: Deploy from a branch**, branch **`main`**, folder **`/ (root)`**, lalu **Save**.
4. Tunggu 1–2 menit. Situs akan tayang di:
   **https://aqzalfauzan.github.io/ayampotong.bugiyo.github/**

## Memakai domain sendiri (mis. `ayampotongbugiyo.com`)

1. Beli domain di registrar mana pun (Niagahoster, Rumahweb, Cloudflare, Namecheap, dll.).
2. Di pengaturan DNS domain tersebut tambahkan:
   - 4 record **A** untuk `@` → `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - 1 record **CNAME** untuk `www` → `aqzalfauzan.github.io`
3. Di **Settings → Pages → Custom domain**, isi domain Anda lalu **Save**, dan centang **Enforce HTTPS** setelah tersedia.
4. Ganti semua `https://aqzalfauzan.github.io/ayampotong.bugiyo.github/` di file HTML, `feed.xml`, `sitemap.xml`, dan `robots.txt` dengan alamat domain baru (cari-dan-ganti sekali jalan).

Opsi lain yang juga gratis: nama repo `aqzalfauzan.github.io` akan memberi alamat pendek `https://aqzalfauzan.github.io/`.

## Menambah artikel baru

1. Salin `artikel/bisnis-ayam-potong-lampung-2026.html` menjadi file baru di folder `artikel/`, lalu ganti judul, deskripsi, tanggal, label, dan isinya.
2. Tambahkan kartu artikel baru di `index.html` (di dalam `data-post-list`, di atas artikel lama) dan perbarui widget **Artikel terbaru**, **Label**, dan **Arsip** di sidebar.
3. Tambahkan `<item>` baru di `feed.xml` dan `<url>` baru di `sitemap.xml`.
4. Opsional: buat gambar sampul 1200×630 piksel di `assets/img/` untuk pratinjau WhatsApp/Facebook.
