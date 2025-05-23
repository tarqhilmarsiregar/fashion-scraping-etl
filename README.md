# Fashion Data ETL Pipeline: Web Scraping to Insights

Membangun **ETL pipeline sederhana** untuk data **fashion** melalui *web scraping*. Data diekstrak, ditransformasi sesuai kebutuhan, dan disimpan dalam format **CSV, SQL, serta TXT** untuk analisis *insight* pasar.

## Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Teknologi yang Digunakan](#teknologi-yang-digunakan)
- [Struktur Proyek](#struktur-proyek)
- [Cara Menjalankan Proyek](#cara-menjalankan-proyek)
- [Contoh Hasil Data](#contoh-hasil-data)
- [Insight yang Diperoleh](#insight-yang-diperoleh)
- [Lisensi](#lisensi)

## Fitur Utama

- **Web Scraping Otomatis**: Mengekstrak data produk fashion (Title, Price, Rating, Colors, Size,Gender) dari situs e-commerce tertentu.
- **Transformasi Data**: Melakukan pembersihan, normalisasi, dan restrukturisasi data untuk memastikan kualitas dan konsistensi.
- **Penyimpanan**: Menyimpan data hasil ETL ke dalam tiga jenis penyimpanan berbeda:
    - `.csv`: Untuk analisis data tabular mudah.
    - `sql`: Untuk integrasi ke database relasional.
    - `Google Spreadsheets`: Untuk berbagi data yang telah diproses secara kolaboratif dan visualisasi cepat, memudahkan pemantauan insight.
- **Modul Reusable**: Kode terstruktur untuk kemudahan pemeliharaan dan pengembangan lebih lanjut.

## Teknologi yang Digunakan

- **Bahasa Pemrograman**: Python
- **Library Python**:
    - `BeautifulSoup` & `Requests`: Untuk web scraping.
    - `Pandas`: Untuk manipulasi dan transformasi data.
    - `datetime`: Untuk manipulasi tanggal dan waktu, seperti timestamp data atau pemformatan waktu.
    - `google-auth-oauthlib` & `google-api-python-client`: Digunakan untuk otentikasi dan interaksi dengan Google Cloud APIs
    - `SQLAlchemy`: Untuk berinteraksi dengan database SQL secara object-relational mapping (ORM) atau sebagai SQL Expression Language, digunakan untuk load data ke format SQL.
    - `python-dotenv`: memuat variabel lingkungan (environment variables) dari sebuah file .env ke dalam lingkungan sistem (environment) tempat aplikasi Python berjalan
- **Database**: PostgreSQL

## Struktur Proyek
```
.
├── utils/
│   ├── __init__.py            # Mengidentifikasi 'utils' sebagai package Python
│   ├── extract.py             # Modul untuk fungsi web scraping (extract)
│   ├── transform.py           # Modul untuk fungsi transformasi data
│   └── load.py                # Modul untuk fungsi penyimpanan data (load ke CSV, SQL, Google Sheets)
├── main.py                    # Script utama untuk menjalankan alur ETL
├── .env                       # File konfigurasi sensitif (diabaikan oleh .gitignore)
├── .gitignore                 # Mengabaikan file/folder yang tidak perlu di commit
└── requirements.txt           # Daftar dependensi Python
```

## Cara Menjalankan Proyek

Ikuti langkah-langkah berikut untuk menjalankan ETL pipeline ini di mesin lokal Anda:

1.  **Clone Repositori:**
    ```bash
    git clone https://github.com/tarqhilmarsiregar/fashion-scraping-etl.git
    cd fashion-scraping-etl
    ```

2.  **Buat Virtual Environment (Direkomendasikan):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # atau
    .\venv\Scripts\activate   # Windows
    ```

3.  **Instal Dependensi:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Konfigurasi:**
    Buat file `.env` di root direktori proyek Anda dan tambahkan variabel lingkungan yang diperlukan
    ```
    SPREADSHEET_ID=INPUT_ID_GOOGLE_SPREADSHEETS
    HOST=INPUT_DATABASE_HOST
    PORT=INPUT_DATABASE_PORT
    DATABASE=INPUT_DATABASE_NAME
    USER=INPUT_DATABASE_USER
    PASSWORD=INPUT_DATABASE_PASSWORD
    ```

5.  **Jalankan Pipeline ETL:**
    ```bash
    python main.py
    ```

    Setelah berjalan, Anda akan menemukan file `products.csv` di dalam folder `fashion-scraping-etl/`.

## Contoh Hasil Data

Berikut adalah cuplikan data yang sudah ditransformasi (dari `products.csv`):

|    Title    |   Price   | Rating | Colors | Size | Gender | Timestamp                  |
|:-----------:|:---------:|:------:|--------|------|--------|----------------------------|
| T-shirt 2   | 1634400.0 | 3.9    | 3      | M    | Women  | 2025-04-27T11:37:53.408827 |
| Hoodie 3    | 7950080.0 | 4.8    | 3      | L    | Unisex | 2025-04-27T11:37:53.408827 |
| Pants 4     | 7476960.0 | 3.3    | 3      | XL   | Men    | 2025-04-27T11:37:53.408827 |
| Outerwear 5 | 5145440.0 | 3.5    | 3      | XXL  | Women  | 2025-04-27T11:37:53.408827 |
| Jacket 6    | 2453920.0 | 3.3    | 3      | S    | Unisex | 2025-04-27T11:37:53.408827 |

## Insight yang Diperoleh

Data yang dihasilkan dari pipeline ETL ini dapat dimanfaatkan untuk berbagai *insight* dan aplikasi bisnis, antara lain:

- **Analisis Tren Harga Produk**: Memantau fluktuasi harga produk (Price) dari berbagai kategori (Title), membantu identifikasi strategi harga atau diskon yang efektif.
- **Preferensi Konsumen Berdasarkan Jenis Kelamin & Ukuran**: Menganalisis preferensi ukuran (Size) dan gender (Gender) untuk produk tertentu, yang dapat membantu dalam perencanaan inventaris atau penargetan kampanye pemasaran.
- **Popularitas Produk Berdasarkan Rating**: Mengidentifikasi produk dengan rating tinggi (Rating) yang dapat menunjukkan popularitas atau kualitas yang disukai konsumen, serta tren produk yang sedang diminati.
- **Variasi Warna dan Model**: Memahami preferensi warna (Colors) yang paling sering muncul atau popularitas model produk tertentu berdasarkan data yang dikumpulkan.
- **Perubahan Tren Seiring Waktu**: Dengan adanya timestamp (Timestamp), data ini memungkinkan analisis tren musiman atau jangka panjang mengenai produk, harga, atau preferensi konsumen.

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).