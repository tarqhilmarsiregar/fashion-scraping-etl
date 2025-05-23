import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Muat variabel lingkungan dari file .env
load_dotenv()

# Panggil variabel
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DATABASE = os.getenv('DATABASE')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

# simpan ke csv
def load_data_to_csv(DataFrame, filename='products.csv'):
    """Menyimpan data hasil scraping ke dalam file CSV dengan error handling."""
    try:
        DataFrame.to_csv(filename, index=False)
        print(f"[INFO] Berhasil menyimpan data ke CSV: {filename}")
        return DataFrame
    except Exception as e:
        print(f"[ERROR] Gagal menyimpan data ke file CSV: {e}")
        return pd.DataFrame()  # Kembalikan DataFrame kosong jika gagal  
    
SERVICE_ACCOUNT_FILE = './google-sheets-api.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Contoh penggunaan
if SPREADSHEET_ID:
    print(f"Spreadsheet ID yang dimuat: {SPREADSHEET_ID}")
else:
    print("Spreadsheet ID tidak ditemukan di .env")

RANGE_NAME = 'Sheet1!A2:G'

# simpan ke googlesheets
def load_data_to_googlesheets(DataFrame):
    try:
        # Inisialisasi service Google Sheets
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

        # Konversi DataFrame ke list of lists
        values = DataFrame.values.tolist()

        body = {
            'values': values
        }

        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("[INFO] Berhasil menyimpan data ke Google Sheets")
    except Exception as e:
        print(f"[ERROR] Terjadi error saat upload: {e}")

# simpan ke postgresql
def load_data_to_postgresql(DataFrame):
    # Buat connection string SQLAlchemy
    engine = create_engine(f'postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}')

    # Keterangan:
    # if_exists:
    # - 'replace' → hapus dan buat ulang tabel
    # - 'append'  → tambah data ke tabel
    # - 'fail'    → error kalau tabel sudah ada

    try:
        DataFrame.to_sql('fashion_detail_items', engine, if_exists='replace', index=False)
        print("[INFO] Berhasil menyimpan data ke PostgreSQL")
    except Exception as e:
        print(f"[ERROR] Gagal mengupload data: {e}")
