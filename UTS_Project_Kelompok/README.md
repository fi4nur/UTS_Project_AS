# Online Book Catalog Scraper & Organizer
### Project Ujian Tengah Semester (UTS) - Automation Systems
**Program Studi Teknik Informatika - Universitas Pelita Bangsa**  
**Tahun Akademik 2025 / 2026**

---

## 📌 Deskripsi Proyek
Aplikasi otomatisasi berbasis Python dengan antarmuka **Command Line Interface (CLI)** untuk mengekstrak katalog buku dari website [Books to Scrape](https://books.toscrape.com/). Program ini mengintegrasikan 5 bab utama materi otomatisasi:
1. **Chapter 9: Regular Expressions (`re`)** — Pembersihan nominal harga desimal, validasi format URL, dan penyaringan kata kunci pencarian judul (case-insensitive).
2. **Chapter 10: Reading and Writing Files (`open`, `csv`, `pathlib`)** — Penyimpanan data mentah ke `.txt`, data terstruktur ke `.csv`, dan penyusunan laporan ringkasan otomatis `laporan.txt` dengan penanganan `FileNotFoundError`.
3. **Chapter 11: Organizing Files (`pathlib`, `zipfile`)** — Pembuatan direktori secara otomatis (`data/`, `output/`, `backup/`) dan pengarsipan kompresi otomatis ke dalam `backup_data.zip`.
4. **Chapter 12: Command Line Programs (`argparse`)** — Manajemen argumen baris perintah lengkap (`--url`, `--keyword`, `--limit`, `--output`, `--backup`).
5. **Chapter 13: Web Scraping (`requests`, `BeautifulSoup`)** — Pengambilan data multi-halaman (paginasi otomatis), penanganan status HTTP, timeout, dan ekstraksi metadata buku (judul, harga, rating, stok, tautan).

---

## 📂 Struktur Direktori Pengumpulan
Sesuai dengan ketentuan format pengumpulan pada lembar soal UTS:

```text
UTS_Project_Kelompok_01/
│
├── main.py                     # Skrip program utama CLI
├── requirements.txt            # Daftar pustaka dependensi Python
├── README.md                   # Petunjuk instalasi dan cara penggunaan
│
├── data/
│   └── raw_data.txt            # Data mentah hasil scraping
│
├── output/
│   ├── hasil_scraping.csv      # Dataset rapi hasil ekstraksi dan regex
│   └── laporan.txt             # Laporan ringkasan pemrosesan dan statistik
│
├── backup/
│   └── backup_data.zip         # Arsip zip berisi data dan output
│
└── dokumentasi/
    ├── laporan_uts.pdf         # Laporan resmi UTS dalam format PDF
    └── LAPORAN_UTS.md          # Dokumen laporan resmi versi Markdown
```

---

## ⚙️ Persyaratan Sistem & Instalasi

### 1. Prasyarat
- Python 3.10 atau versi yang lebih baru.
- Koneksi internet aktif untuk proses scraping web.

### 2. Langkah Instalasi Dependensi
Buka terminal pada direktori proyek, lalu jalankan:

```bash
# Opsi 1: Menggunakan Virtual Environment (Disarankan)
python -m venv venv
venv\Scripts\activate       # Pada Windows
source venv/bin/activate    # Pada Linux/macOS

# Opsi 2: Instalasi pustaka langsung
pip install -r requirements.txt
```

---

## 🚀 Panduan Penggunaan CLI

Jalankan program melalui terminal / command prompt dengan perintah `python main.py`.

### Argumen CLI yang Tersedia:
| Argumen | Tipe | Default | Keterangan |
|---|---|---|---|
| `--url` | String | `https://books.toscrape.com/` | URL target website katalog buku. |
| `--keyword` | String | `""` (Kosong) | Kata kunci untuk memfilter judul buku menggunakan Regex. |
| `--limit` | Integer | `30` | Batas minimal jumlah buku yang diambil (minimal 30). |
| `--output` | String | `hasil_scraping.csv` | Nama file keluaran CSV di folder `output/`. |
| `--backup` | Flag | `False` | Mengaktifkan pembuatan arsip kompresi `.zip` otomatis. |

### Contoh Pemanggilan Perintah:

1. **Pengambilan Standar (30 Record + Backup Otomatis):**
   ```bash
   python main.py --backup
   ```

2. **Pengambilan Sesuai Contoh Soal UTS:**
   ```bash
   python main.py --url https://books.toscrape.com/ --keyword the --limit 30 --backup
   ```

3. **Pencarian Spesifik dengan Limit Custom:**
   ```bash
   python main.py --keyword history --limit 50 --backup
   ```

4. **Menampilkan Menu Bantuan CLI:**
   ```bash
   python main.py --help
   ```

---

## 🛡️ Penanganan Kesalahan (Error Handling)
Program telah dilengkapi dengan mekanisme mitigasi kegagalan sesuai rubrik penilaian:
1. **Kegagalan Koneksi Jaringan & HTTP:** Ditangani dengan `requests.exceptions.RequestException`, `ConnectionError`, dan `Timeout` tanpa membuat program crash.
2. **Data Kosong:** Program mengecek ketersediaan data sebelum penyimpanan dan memberikan peringatan informatif jika filter tidak menemukan kecocokan.
3. **File Tidak Ditemukan (`FileNotFoundError`):** Ditangani saat pembacaan kembali berkas CSV untuk penyusunan laporan ringkasan teks.
4. **Encoding Terminal Windows:** Dilengkapi konfigurasi otomatis UTF-8 untuk mencegah `UnicodeEncodeError` pada terminal bawaan Windows.

---
