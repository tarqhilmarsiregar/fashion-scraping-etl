import pandas as pd

def transform_to_DataFrame(data):
    """Mengubah data menjadi DataFrame dengan error handling."""
    try:
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"[ERROR] Gagal mengubah data ke DataFrame: {e}")
        return pd.DataFrame()  # Kembalikan DataFrame kosong kalau gagal
    
def transform_data(data, exchange_rate):
    """Mengubah data menjadi DataFrame, menghapus duplikat, lalu membersihkan data dengan error handling."""
    try:
        # Ubah ke DataFrame
        df = transform_to_DataFrame(data)

        if df.empty:
            print("[WARNING] Data kosong, tidak ada yang perlu ditransformasi.")
            return df
        else:
            # Hapus duplikat
            df = df.drop_duplicates()

        # Copy data untuk transformasi
        clean_data = df.copy()

        # Pastikan semua kolom yang dibutuhkan ada
        required_columns = ["Title", "Rating", "Price", "Colors"]
        for col in required_columns:
            if col not in clean_data.columns:
                raise KeyError(f"Kolom '{col}' tidak ditemukan di data.")

        # Pola data kotor yang ingin dibersihkan
        dirty_patterns = {
            "Title": ["Unknown Product"],
            "Rating": ["Invalid Rating / 5", "Not Rated"],
            "Price": ["Price Unavailable", None]
        }

        # Hapus data dengan nilai tidak valid
        for column, dirty_values in dirty_patterns.items():
            clean_data = clean_data[~clean_data[column].isin(dirty_values)]

        # Bersihkan dan konversi kolom Price
        try:
            clean_data['Price'] = clean_data['Price'].str.replace('$', '', regex=False)
            clean_data['Price'] = pd.to_numeric(clean_data['Price'], errors='coerce')  # NaN jika gagal
            clean_data.dropna(subset=['Price'], inplace=True)
            clean_data['Price'] = (clean_data['Price'] * exchange_rate).round(2)
        except Exception as e:
            print(f"[ERROR] Gagal memproses kolom 'Price': {e}")

        # Bersihkan dan konversi kolom Colors
        try:
            clean_data['Colors'] = pd.to_numeric(clean_data['Colors'], errors='coerce')
            clean_data.dropna(subset=['Colors'], inplace=True)
            clean_data['Colors'] = clean_data['Colors'].astype(int)
        except Exception as e:
            print(f"[ERROR] Gagal memproses kolom 'Colors': {e}")

        # Bersihkan dan konversi kolom Rating
        try:
            clean_data['Rating'] = clean_data['Rating'].str.extract(r'([0-9.]+)')
            clean_data['Rating'] = pd.to_numeric(clean_data['Rating'], errors='coerce')
            clean_data.dropna(subset=['Rating'], inplace=True)
        except Exception as e:
            print(f"[ERROR] Gagal memproses kolom 'Rating': {e}")

        return clean_data

    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan saat transformasi data: {e}")
        return pd.DataFrame()