from utils import scrape_up_to_50_pages, transform_data, load_data_to_csv, load_data_to_googlesheets, load_data_to_postgresql

def main():
    """Fungsi utama untuk menjalankan proses scraping dan menyimpan data."""
    url = 'https://fashion-studio.dicoding.dev/'
    fashion_data = scrape_up_to_50_pages(url)

    if fashion_data:
        DataFrame = transform_data(fashion_data, 16000)
        load_data_to_csv(DataFrame)
        load_data_to_googlesheets(DataFrame)
        load_data_to_postgresql(DataFrame)
    else:
        print("Tidak ada data yang ditemukan.")

if __name__ == "__main__":
    main()