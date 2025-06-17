import requests 
import pandas as pd 
from datetime import datetime, timedelta, timezone
import os
import numpy as np

def get_date_range(days_back, hours):
    """Mengembalikan rentang tanggal dalam format  (YYYY-MM-DD)."""
    today = datetime.now(timezone.utc) + timedelta(hours=hours)
    yesterday = today - timedelta(days=days_back)
    return yesterday.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")

def fetch_timeseries(symbol, TWELVE_API_KEY, interval="1min", outputsize=5000, start_date=None, end_date=None):
    
    url = "https://api.twelvedata.com/time_series"

    params = {
        "symbol": symbol,
        "interval": interval,
        "outputsize": outputsize,
        "apikey": TWELVE_API_KEY,
        "start_date": start_date,
        "end_date": end_date
    }

    print(f"[INFO] Requesting data for {symbol} ({interval}) from {start_date} to {end_date}")
    response = requests.get(url, params=params)
    return response.json()

def save_timeseries_to_csv(data, symbol, output_dir):
    if "values" not in data:
        print("[X] Gagal mengambil data:", data.get("message", "Unknown error"))
        return
    
    df = pd.DataFrame(data["values"])
    df["datetime"] = pd.to_datetime(df["datetime"])
    df.set_index("datetime", inplace=True)
    df.sort_index(inplace=True)
    df["symbol"] = symbol 

    filename = f"{symbol.replace('/', '_')}.csv"
    
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath)
    print(f"[✓] Data {symbol} berhasil disimpan sebagai {filename}")


def get_and_save_data(symbol, output_dir,TWELVE_API_KEY, interval="1min",hours=1, days_back=1):

    start_date, end_date = get_date_range(days_back=days_back, hours=hours)
    data = fetch_timeseries(symbol, TWELVE_API_KEY, interval, start_date=start_date,end_date=end_date)
    save_timeseries_to_csv(data, symbol,output_dir)



def load_minute_data(filepath):
    """Membaca data per-menit dari file CSV."""
    return pd.read_csv(filepath, parse_dates=["datetime"])

def generate_second_level_data(minute_df):
    """Mengonversi data per-menit menjadi data per-detik (60 titik data per menit)."""
    data_per_second = []

    for _, row in minute_df.iterrows():
        base_time = row["datetime"]
        open_price = float(row["open"])
        high_price = float(row["high"])
        low_price = float(row["low"])
        close_price = float(row["close"])
        symbol = row["symbol"]

        # Tambahkan data HH:MM:00 asli
        data_per_second.append({
            "datetime": base_time,
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "symbol": symbol
        })

        # Tambahkan data HH:MM:01 sampai HH:MM:59 dengan nilai acak
        for i in range(1, 60):
            second_time = base_time + timedelta(seconds=i)

            o = np.round(np.random.uniform(low_price, high_price), 5)
            c = np.round(np.random.uniform(low_price, high_price), 5)
            l = np.round(min(o, c, np.random.uniform(low_price, high_price)), 5)
            h = np.round(max(o, c, np.random.uniform(low_price, high_price)), 5)

            data_per_second.append({
                "datetime": second_time,
                "open": o,
                "high": h,
                "low": l,
                "close": c,
                "symbol": symbol
            })

    return pd.DataFrame(data_per_second)

def save_to_csv(df, output_path):
    """Menyimpan DataFrame ke file CSV."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Selesai. File disimpan di: {output_path}")

def convert_minute_to_second_csv(symbol, input_dir, output_dir ):
    """Fungsi utama: dari file per-menit ke file per-detik."""
    input_csv = os.path.join(input_dir, f"{symbol.replace('/', '_')}.csv")
    output_csv = os.path.join(output_dir, f"{symbol.replace('/', '_')}_update.csv")
    df_minute = load_minute_data(input_csv)
    df_second = generate_second_level_data(df_minute)
    save_to_csv(df_second, output_csv)

def combine_and_sort_csv(input_path: str) -> pd.DataFrame:
    """
    Membaca semua file CSV di input_path, menggabungkan semuanya, 
    dan mengurutkannya berdasarkan kolom datetime.
    
    :param input_path: Path ke direktori yang berisi file-file CSV
    :return: DataFrame gabungan yang sudah diurutkan berdasarkan kolom datetime
    """
    all_dfs = []

    for filename in os.listdir(input_path):
        if filename.endswith('.csv'):
            filepath = os.path.join(input_path, filename)
            df = pd.read_csv(filepath, parse_dates=['datetime'])
            all_dfs.append(df)

    if not all_dfs:
        raise ValueError("Tidak ada file CSV ditemukan di direktori.")

    combined_df = pd.concat(all_dfs, ignore_index=True)
    combined_df = combined_df.sort_values(by='datetime')
    return combined_df


