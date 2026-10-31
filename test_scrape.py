import requests
from bs4 import BeautifulSoup

def test_page(url):
    print(f"Sedang mencoba mengambil data dari: {url}...")
    try:
        # Mengambil data dari website
        resp = requests.get(url, timeout=10)
        print(f"Status koneksi: {resp.status_code} (200 artinya sukses)")
        
        # Merapikan teks HTML agar mudah dibaca program
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("article.product_pod")
        print(f"Jumlah buku ditemukan di halaman ini: {len(cards)}")
        
        if cards:
            c = cards[0]
            print("--- Contoh 1 Buku ---")
            print(f"Judul  : {c.h3.a['title']}")
            print(f"Harga  : {c.select_one('p.price_color').get_text(strip=True)}")
            print(f"Rating : {c.select_one('p.star-rating')['class']}")
            print("----------------------")
    except Exception as e:
        print(f"Waduh, ada error: {e}")

# Kita tes ambil dari Halaman 1 dan Halaman 2
print("=== MULAI TES SCRAPING ===")
test_page("https://books.toscrape.com/catalogue/page-1.html")
test_page("https://books.toscrape.com/catalogue/page-2.html")
print("=== TES SELESAI ===")