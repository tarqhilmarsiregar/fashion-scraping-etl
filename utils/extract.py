import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Tambahkan user-agent ke dalam header untuk menghindari blokir oleh server
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def extract_fashion_data(detail):
    """Mengekstrak data fashion dengan penanganan error sederhana"""
    try:
        # Title
        title_tag = detail.find('h3', class_='product-title')
        title = title_tag.text.strip() if title_tag else 'No Title'

        # Price
        price_tag = detail.find('span', class_='price')
        price = price_tag.text.strip() if price_tag else 'Price Unavailable'

        # Default values
        rating = 'Not Available'
        colors = 'Not Specified'
        size = 'Not Specified'
        gender = 'Unisex'

        # Info tambahan
        info_tags = detail.find_all('p')
        for tag in info_tags:
            text = tag.text.strip()

            if text.startswith('Rating:'):
                rating = text.replace('Rating:', '').strip()
            elif 'Colors' in text:
                colors = text.replace('Colors', '').strip()
            elif 'Size:' in text:
                size = text.replace('Size:', '').strip()
            elif 'Gender:' in text:
                gender = text.replace('Gender:', '').strip()

        # Timestamp
        timestamp = datetime.now().isoformat()

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp        
        }
    except Exception as e:
        print(f"[ERROR] Gagal mengekstrak data fashion: {e}")
        return {
            "Title": 'Error',
            "Price": 'Error',
            "Rating": 'Error',
            "Colors": 'Error',
            "Size": 'Error',
            "Gender": 'Error',
            "Timestamp": datetime.now().isoformat()
        }



def fetch_page_content(url):
    """Mengambil konten HTML dari URL dengan user-agent yang ditentukan."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Memunculkan HTTPError untuk status yang buruk
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error saat mengambil {url}: {e}")
        return None

def scrape_fashion_data(url):
    """Melakukan scraping untuk semua data fashion"""
    try:
        content = fetch_page_content(url)
        if not content:
            print(f"[WARNING] Gagal mengambil konten dari {url}")
            return []

        soup = BeautifulSoup(content, 'html.parser')
        data = []

        collection_cards = soup.find_all('div', class_='collection-card')
        if not collection_cards:
            print(f"[INFO] Tidak ditemukan koleksi fashion di {url}")
            return []

        for card in collection_cards:
            try:
                product_details = card.find_all(class_='product-details')
                for detail in product_details:
                    try:
                        fashion_data = extract_fashion_data(detail)
                        data.append(fashion_data)
                    except Exception as e:
                        print(f"[ERROR] Gagal extract data produk: {e}")
            except Exception as e:
                print(f"[ERROR] Gagal mengambil detail produk: {e}")

        return data

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat scraping {url}: {e}")
        return []


def scrape_up_to_50_pages(base_url, max_pages=50):
    """Melakukan scraping dari halaman 1 sampai 50 atau sampai tidak ada data"""
    all_data = []

    # Scraping halaman pertama tanpa 'page' parameter
    print(f"[INFO] Scraping halaman 1: {base_url}")
    try:
        page_data = scrape_fashion_data(base_url)
        if page_data:
            all_data.extend(page_data)
        else:
            print("[INFO] Tidak ada data ditemukan di halaman pertama.")
            return all_data  # Jika tidak ada data di halaman pertama, berhenti
    except Exception as e:
        print(f"[ERROR] Gagal scraping halaman pertama: {e}")
        return all_data  # Jika gagal pada halaman pertama, return data yang sudah terkumpul

    # Scraping halaman-halaman berikutnya (halaman 2 sampai max_pages)
    for page in range(2, max_pages + 1):
        url = f"{base_url}page{page}"
        print(f"[INFO] Scraping halaman {page}: {url}")

        try:
            page_data = scrape_fashion_data(url)
            if not page_data:
                print("[INFO] Tidak ada data ditemukan di halaman ini. Berhenti.")
                break
            all_data.extend(page_data)
        except Exception as e:
            print(f"[ERROR] Gagal scraping halaman {page}: {e}")
            continue  # lanjutkan ke halaman berikutnya meskipun error

    return all_data