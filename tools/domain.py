#!/usr/bin/env python3
"""Cek, daftarkan, dan hubungkan domain ke GitHub Pages lewat API Porkbun.

Hanya memakai pustaka bawaan Python 3.8+, tanpa instalasi apa pun.

Siapkan dulu (sekali saja):
  1. Buat akun di https://porkbun.com, verifikasi email dan nomor HP.
  2. Isi saldo (account credit) di https://porkbun.com/account/credit.
     Pendaftaran lewat API dibayar dari saldo ini, bukan langsung dari kartu.
  3. Buat API key di https://porkbun.com/account/api, lalu set:
       export PORKBUN_API_KEY="pk1_..."
       export PORKBUN_SECRET_API_KEY="sk1_..."
     (Windows PowerShell: $env:PORKBUN_API_KEY="pk1_...")
     Untuk mencoba tanpa uang sungguhan, pakai sandbox key (pk1_sb_ / sk1_sb_).

Perintah:
  python3 tools/domain.py cek                    # cek nama blog di beberapa ekstensi
  python3 tools/domain.py cek ayampotongbugiyo.com
  python3 tools/domain.py daftar ayampotongbugiyo.com
  python3 tools/domain.py hubungkan ayampotongbugiyo.com
  python3 tools/domain.py periksa ayampotongbugiyo.com
"""
import argparse
import json
import os
import pathlib
import socket
import sys
import time
import urllib.error
import urllib.request
import uuid
from decimal import Decimal

API = os.environ.get("PORKBUN_API_BASE", "https://api.porkbun.com/api/json/v3")
NAMA = "ayampotongbugiyo"
EKSTENSI = ["com", "net", "org", "blog", "site", "online", "store", "xyz"]

GITHUB_USER = "aqzalfauzan"
GITHUB_HOST = f"{GITHUB_USER}.github.io"
ALAMAT_LAMA = f"https://{GITHUB_HOST}/ayampotong.bugiyo.github/"
# Alamat IP resmi GitHub Pages:
# https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
GITHUB_A = ["185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"]
GITHUB_AAAA = ["2606:50c0:8000::153", "2606:50c0:8001::153", "2606:50c0:8002::153", "2606:50c0:8003::153"]

REPO = pathlib.Path(__file__).resolve().parent.parent
FILE_SITUS = ["index.html", "tentang.html", "404.html", "artikel-ayam-potong-lampung.html",
              "feed.xml", "sitemap.xml", "robots.txt"]


class ApiError(Exception):
    pass


def kunci():
    k, s = os.environ.get("PORKBUN_API_KEY"), os.environ.get("PORKBUN_SECRET_API_KEY")
    if not k or not s:
        sys.exit("PORKBUN_API_KEY dan PORKBUN_SECRET_API_KEY belum di-set. "
                 "Buat di https://porkbun.com/account/api (lihat petunjuk di atas file ini).")
    return k, s


def panggil(path, body=None, idempotent=False, coba=3):
    k, s = kunci()
    data = json.dumps({**(body or {}), "apikey": k, "secretapikey": s}).encode()
    headers = {"Content-Type": "application/json", "Accept": "application/json",
               "User-Agent": "ayampotong-bugiyo-domain/1.0"}
    if idempotent:
        # kunci yang sama dipakai untuk semua percobaan ulang, jadi tidak tertagih dua kali
        headers["Idempotency-Key"] = str(uuid.uuid4())
    for i in range(coba):
        req = urllib.request.Request(API + path, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                hasil = json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < coba - 1:
                tunggu = int(e.headers.get("Retry-After") or 10)
                print(f"  (dibatasi API, menunggu {tunggu} detik...)")
                time.sleep(tunggu)
                continue
            try:
                hasil = json.loads(e.read() or b"{}")
            except ValueError:
                raise ApiError(f"HTTP {e.code}")
        except urllib.error.URLError as e:
            raise ApiError(f"Tidak bisa menghubungi Porkbun: {e.reason}")
        if hasil.get("status") != "SUCCESS":
            kode = f" [{hasil['code']}]" if hasil.get("code") else ""
            raise ApiError(f"{hasil.get('message', 'gagal')}{kode}")
        return hasil
    raise ApiError("terlalu sering dibatasi API, coba lagi nanti")


def cek_satu(domain):
    r = panggil(f"/domain/checkDomain/{domain}")["response"]
    return {
        "domain": domain,
        "tersedia": r.get("avail") == "yes",
        "premium": r.get("premium") == "yes",
        "harga": r.get("price"),
        "perpanjang": r.get("regularPrice") or (r.get("additional", {}).get("renewal", {}) or {}).get("price"),
    }


def cmd_cek(args):
    domains = args.domain or [f"{NAMA}.{t}" for t in EKSTENSI]
    print(f"{'Domain':32} {'Status':14} {'Tahun 1':>9} {'Perpanjang':>11}")
    for i, d in enumerate(domains):
        if i:
            time.sleep(1.2)  # batas API: sekitar 10 cek per 10 detik
        try:
            c = cek_satu(d.lower())
        except ApiError as e:
            print(f"{d:32} galat: {e}")
            continue
        status = "premium" if c["premium"] else ("TERSEDIA" if c["tersedia"] else "sudah dipakai")
        harga = f"${c['harga']}" if c["tersedia"] and c["harga"] else "-"
        renew = f"${c['perpanjang']}" if c["tersedia"] and c["perpanjang"] else "-"
        print(f"{d:32} {status:14} {harga:>9} {renew:>11}")
    print("\nHarga dalam dolar AS per tahun. Domain premium tidak bisa didaftarkan lewat API.")


def cmd_daftar(args):
    d = args.domain.lower()
    c = cek_satu(d)
    if not c["tersedia"]:
        sys.exit(f"{d} tidak tersedia.")
    if c["premium"]:
        sys.exit(f"{d} adalah domain premium; daftarkan lewat situs porkbun.com.")
    sen = int((Decimal(c["harga"]) * 100).to_integral_value())

    print(f"{d} tersedia. Biaya tahun pertama: ${c['harga']}"
          + (f", perpanjangan: ${c['perpanjang']}/tahun" if c["perpanjang"] else ""))

    # uji dulu tanpa menagih: memeriksa harga, saldo, dan syarat akun
    try:
        uji = panggil(f"/domain/create/{d}", {"cost": sen, "agreeToTerms": "yes", "dryRun": True})
        if uji.get("wouldSucceed") is False:
            sys.exit("Uji coba gagal: " + json.dumps(uji, ensure_ascii=False))
        print("Uji coba (tanpa menagih) berhasil: saldo dan data akun cukup.")
    except ApiError as e:
        sys.exit(f"Uji coba gagal: {e}")

    if not args.ya:
        jawab = input(f"\nKetik nama domain ({d}) untuk membeli dan memotong saldo ${c['harga']}: ").strip().lower()
        if jawab != d:
            sys.exit("Dibatalkan. Tidak ada yang dibeli.")

    hasil = panggil(f"/domain/create/{d}", {"cost": sen, "agreeToTerms": "yes"}, idempotent=True)
    print(f"\nBerhasil! {d} sudah terdaftar di akun Porkbun Anda.")
    print(json.dumps(hasil, indent=2, ensure_ascii=False))
    print(f"\nLangkah berikutnya: python3 tools/domain.py hubungkan {d}")


def cmd_hubungkan(args):
    d = args.domain.lower()
    records = panggil(f"/dns/retrieve/{d}").get("records", [])

    # hapus record bawaan (parkir Porkbun) di root, www, dan wildcard yang akan bentrok
    nama_bentrok = {d, f"www.{d}", f"*.{d}"}
    for r in records:
        if r.get("name") in nama_bentrok and r.get("type") in ("A", "AAAA", "ALIAS", "CNAME"):
            print(f"  hapus {r['type']:5} {r['name']} -> {r['content']}")
            panggil(f"/dns/delete/{d}/{r['id']}")

    baru = [("", "A", ip) for ip in GITHUB_A] + [("", "AAAA", ip) for ip in GITHUB_AAAA] + [("www", "CNAME", GITHUB_HOST)]
    for name, typ, content in baru:
        print(f"  buat  {typ:5} {(name + '.' if name else '') + d} -> {content}")
        panggil(f"/dns/create/{d}", {"name": name, "type": typ, "content": content, "ttl": "600"}, idempotent=True)

    # file CNAME + ganti alamat lengkap di situs
    (REPO / "CNAME").write_text(d + "\n")
    baru_url = f"https://{d}/"
    diubah = []
    for f in FILE_SITUS + [str(p.relative_to(REPO)) for p in (REPO / "artikel").glob("*.html")]:
        p = REPO / f
        if p.exists():
            teks = p.read_text(encoding="utf-8")
            if ALAMAT_LAMA in teks:
                p.write_text(teks.replace(ALAMAT_LAMA, baru_url), encoding="utf-8")
                diubah.append(f)
    print(f"\nDNS sudah diarahkan ke GitHub Pages. File CNAME dibuat; alamat diganti di: {', '.join(diubah) or '-'}")
    print(f"""
Langkah berikutnya:
  1. git add -A && git commit -m "Pakai domain {d}" && git push
  2. GitHub: Settings > Pages > Custom domain: isi {d} > Save
  3. Tunggu "DNS check successful" (beberapa menit sampai 24 jam), lalu centang Enforce HTTPS
  4. Cek: python3 tools/domain.py periksa {d}""")


def cmd_periksa(args):
    d = args.domain.lower()
    ok = True
    try:
        ips = sorted({ai[4][0] for ai in socket.getaddrinfo(d, 443, socket.AF_INET)})
    except socket.gaierror:
        ips = []
    cocok = bool(ips) and set(ips) <= set(GITHUB_A)
    print(f"{d}: {', '.join(ips) or 'belum ditemukan'} -> {'OK' if cocok else 'belum mengarah ke GitHub'}")
    ok &= cocok
    try:
        www = socket.gethostbyname_ex(f"www.{d}")
        cocok_www = GITHUB_HOST in www[1] or set(www[2]) <= set(GITHUB_A)
    except socket.gaierror:
        www, cocok_www = None, False
    print(f"www.{d}: {'OK' if cocok_www else 'belum mengarah ke ' + GITHUB_HOST}")
    ok &= cocok_www
    cname = REPO / "CNAME"
    isi = cname.read_text().strip() if cname.exists() else ""
    print(f"File CNAME: {isi or 'tidak ada'} -> {'OK' if isi == d else 'harus berisi ' + d}")
    ok &= isi == d
    if not ok:
        print("\nDNS baru bisa butuh beberapa menit sampai 24 jam untuk menyebar. Coba lagi nanti.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser(description="Cek, daftarkan, dan hubungkan domain ke GitHub Pages (Porkbun).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("cek", help="cek ketersediaan dan harga")
    p.add_argument("domain", nargs="*", help=f"default: {NAMA} dengan ekstensi {', '.join(EKSTENSI)}")
    p.set_defaults(fn=cmd_cek)
    p = sub.add_parser("daftar", help="beli domain (memotong saldo Porkbun)")
    p.add_argument("domain")
    p.add_argument("--ya", action="store_true", help="lewati konfirmasi ketik ulang nama domain")
    p.set_defaults(fn=cmd_daftar)
    p = sub.add_parser("hubungkan", help="arahkan DNS ke GitHub Pages dan buat file CNAME")
    p.add_argument("domain")
    p.set_defaults(fn=cmd_hubungkan)
    p = sub.add_parser("periksa", help="periksa apakah domain sudah mengarah ke GitHub Pages")
    p.add_argument("domain")
    p.set_defaults(fn=cmd_periksa)
    args = ap.parse_args()
    try:
        args.fn(args)
    except ApiError as e:
        sys.exit(f"Galat dari Porkbun: {e}")


if __name__ == "__main__":
    main()
