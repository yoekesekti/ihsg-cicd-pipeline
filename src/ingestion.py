
import yfinance as yf
import pandas as pd
from pathlib import Path

from src.validation import validate_data


TICKERS = {
    "^JKSE": "JKSE",
    "CL=F": "CLF",
    "GC=F": "GCF",
    "IDR=X": "IDRX",
    "^DJI": "DJI",
    "^HSI": "HSI",
    "^N225": "N225",
    "EEM": "EEM"
}

START_DATE = "2018-01-01"
OUTPUT_FILE = Path("data/ihsg_historical.csv")


def fetch_data():
    all_data = []

    for ticker, name in TICKERS.items():
        print(f"Mengambil data {name} ({ticker})...")

        data = yf.download(
            ticker,
            start=START_DATE,
            auto_adjust=False,
            progress=False
        )

        if data.empty:
            print(f"Data {ticker} tidak tersedia.")
            continue

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data = data.reset_index()
        data["Ticker"] = ticker
        data["Instrument"] = name

        all_data.append(data)

    if not all_data:
        raise RuntimeError("Tidak ada data yang berhasil diambil.")

    result = pd.concat(all_data, ignore_index=True)

    result["Date"] = pd.to_datetime(
        result["Date"]
    ).dt.strftime("%Y-%m-%d")

    return result


def main():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    new_data = fetch_data()

    if OUTPUT_FILE.exists():
        old_data = pd.read_csv(OUTPUT_FILE)
        combined = pd.concat(
            [old_data, new_data],
            ignore_index=True
        )
    else:
        combined = new_data

    combined = combined.drop_duplicates(
        subset=["Date", "Ticker"],
        keep="last"
    )

    combined = combined.sort_values(
        by=["Date", "Ticker"]
    ).reset_index(drop=True)

    # Memvalidasi data sebelum disimpan
    validate_data(combined)

    combined.to_csv(OUTPUT_FILE, index=False)

    print(f"Total data: {len(combined)} baris")
    print(f"File tersimpan: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
