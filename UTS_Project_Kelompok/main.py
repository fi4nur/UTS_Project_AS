import argparse
import csv
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE = Path(__file__).resolve().parent
DATA, OUTPUT, BACKUP = BASE / "data", BASE / "output", BASE / "backup"


def ambil_buku(url, limit):
    """Scraping katalog; pindah halaman lewat tombol 'next' sampai limit terpenuhi."""
    buku = []
    while url and len(buku) < limit:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"[ERROR] Gagal mengakses {url}: {e}")
            break
        resp.encoding = "utf-8"  # agar simbol £ tidak rusak
        soup = BeautifulSoup(resp.text, "html.parser")

        for card in soup.select("article.product_pod"):
            buku.append({
                "judul": card.h3.a["title"],
                "harga_asli": card.select_one("p.price_color").text.strip(),
                "rating": card.select_one("p.star-rating")["class"][1],
                "stok": card.select_one("p.availability").text.strip(),
                "tautan": urljoin(url, card.h3.a["href"]),
            })

        next_link = soup.select_one("li.next a")
        url = urljoin(url, next_link["href"]) if next_link else None
        print(f"[INFO] Terkumpul {len(buku)} buku")

    return buku[:limit]


def harga_angka(teks):
    """Regex: '£51.77' -> 51.77"""
    m = re.search(r"\d+\.\d{2}", teks)
    return float(m.group()) if m else 0.0


def simpan_data(buku, nama_csv):
    """Simpan raw_data.txt dan file CSV."""
    with open(DATA / "raw_data.txt", "w", encoding="utf-8") as f:
        for b in buku:
            f.write(" | ".join(b.values()) + "\n")

    path_csv = OUTPUT / nama_csv
    with open(path_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Judul", "Harga Asli", "Harga Angka", "Rating", "Ketersediaan", "Tautan"])
        for b in buku:
            w.writerow([b["judul"], b["harga_asli"], harga_angka(b["harga_asli"]),
                        b["rating"], b["stok"], b["tautan"]])
    return path_csv


def buat_laporan(path_csv, keyword):
    """Baca ulang CSV lalu tulis output/laporan.txt."""
    try:
        with open(path_csv, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"[ERROR] File {path_csv} tidak ditemukan, laporan dibatalkan.")
        return

    harga = [float(r["Harga Angka"]) for r in rows]
    rating = {}
    for r in rows:
        rating[r["Rating"]] = rating.get(r["Rating"], 0) + 1

    baris = [
        "LAPORAN HASIL SCRAPING",
        "=" * 50,
        f"Waktu        : {datetime.now():%Y-%m-%d %H:%M:%S}",
        f"Keyword      : {keyword or '(tanpa filter)'}",
        f"Total buku   : {len(rows)}",
        f"Harga rata2  : £{sum(harga) / len(harga):.2f}",
        f"Harga min    : £{min(harga):.2f}",
        f"Harga max    : £{max(harga):.2f}",
        "",
        "Distribusi rating:",
        *[f" - {k}: {v} buku" for k, v in sorted(rating.items())],
        "",
        "5 buku pertama:",
        *[f"{i}. {r['Judul']} (£{r['Harga Angka']}) - {r['Rating']}"
          for i, r in enumerate(rows[:5], 1)],
    ]
    (OUTPUT / "laporan.txt").write_text("\n".join(baris) + "\n", encoding="utf-8")
    print("[SUCCESS] Laporan disimpan: output/laporan.txt")


def buat_backup():
    """Zip semua file di data/ dan output/."""
    with zipfile.ZipFile(BACKUP / "backup_data.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for folder in (DATA, OUTPUT):
            for file in folder.glob("*"):
                zf.write(file, f"{folder.name}/{file.name}")
    print("[SUCCESS] Backup dibuat: backup/backup_data.zip")


def main():
    p = argparse.ArgumentParser(description="Scraper Katalog Buku",
                                epilog="Contoh: python main.py --keyword the --limit 30 --backup")
    p.add_argument("--url", default="https://books.toscrape.com/", help="URL sumber")
    p.add_argument("--keyword", default="", help="Filter judul (regex, case-insensitive)")
    p.add_argument("--limit", type=int, default=30, help="Jumlah buku yang diambil")
    p.add_argument("--output", default="hasil_scraping.csv", help="Nama file CSV di output/")
    p.add_argument("--backup", action="store_true", help="Buat backup ZIP")
    args = p.parse_args()

    if not re.match(r"^https?://\S+$", args.url):
        sys.exit("[ERROR] URL tidak valid, gunakan format http:// atau https://")

    for folder in (DATA, OUTPUT, BACKUP):
        folder.mkdir(exist_ok=True)

    buku = ambil_buku(args.url, args.limit)
    if not buku:
        sys.exit("[WARNING] Tidak ada data yang berhasil diambil.")

    if args.keyword:
        pola = re.compile(re.escape(args.keyword), re.IGNORECASE)
        buku = [b for b in buku if pola.search(b["judul"])]
        print(f"[INFO] Filter '{args.keyword}': {len(buku)} buku cocok")
        if not buku:
            sys.exit("[WARNING] Tidak ada judul yang cocok dengan keyword.")

    path_csv = simpan_data(buku, args.output)
    buat_laporan(path_csv, args.keyword)
    if args.backup:
        buat_backup()

    harga = [harga_angka(b["harga_asli"]) for b in buku]
    print("\n" + "=" * 50)
    print(f"Total buku : {len(buku)}")
    print(f"Rata-rata  : £{sum(harga) / len(harga):.2f}")
    print(f"CSV        : {path_csv}")
    print(f"Backup     : {'dibuat' if args.backup else 'tidak (pakai --backup)'}")
    print("=" * 50)


if __name__ == "__main__":
    main()