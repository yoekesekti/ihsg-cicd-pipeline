
import pandas as pd


REQUIRED_COLUMNS = [
    "Date",
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close",
    "Volume",
    "Ticker",
    "Instrument"
]

EXPECTED_TICKERS = {
    "^JKSE",
    "CL=F",
    "GC=F",
    "IDR=X",
    "^DJI",
    "^HSI",
    "^N225",
    "EEM"
}

PRICE_COLUMNS = [
    "Open",
    "High",
    "Low",
    "Close",
    "Adj Close"
]


def validate_data(df):
    # Memastikan dataset tidak kosong
    if df.empty:
        raise ValueError("Dataset kosong.")

    # Memastikan seluruh kolom tersedia
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Kolom tidak lengkap: {missing_columns}"
        )

    # Memastikan delapan instrumen tersedia
    actual_tickers = set(df["Ticker"].dropna().unique())

    if actual_tickers != EXPECTED_TICKERS:
        raise ValueError(
            f"Daftar ticker tidak sesuai. Ditemukan: {actual_tickers}"
        )

    # Memastikan tanggal valid
    dates = pd.to_datetime(df["Date"], errors="coerce")

    if dates.isna().any():
        raise ValueError("Terdapat tanggal yang tidak valid.")

    # Memastikan tidak ada duplikasi tanggal dan ticker
    if df.duplicated(subset=["Date", "Ticker"]).any():
        raise ValueError("Terdapat data duplikat.")

    # Memastikan kolom numerik berisi nilai valid
    numeric_columns = PRICE_COLUMNS + ["Volume"]

    for column in numeric_columns:
        values = pd.to_numeric(df[column], errors="coerce")

        if values.isna().any():
            raise ValueError(
                f"Kolom {column} memiliki nilai kosong atau tidak valid."
            )

        if column == "Volume" and (values < 0).any():
            raise ValueError(
                "Kolom Volume memiliki nilai negatif."
            )

    ohlc_data = df[df["Ticker"] != "IDR=X"]

    if (ohlc_data["High"] < ohlc_data[["Open", "Close", "Low"]].max(axis=1)).any():
        raise ValueError("Terdapat nilai High yang tidak valid.")

    if (ohlc_data["Low"] > ohlc_data[["Open", "Close", "High"]].min(axis=1)).any():
        raise ValueError("Terdapat nilai Low yang tidak valid.")

    print("Validasi data berhasil.")
    print(f"Total baris: {len(df)}")
    print(f"Jumlah instrumen: {len(actual_tickers)}")

    return True


def validate_file(file_path):
    df = pd.read_csv(file_path)
    return validate_data(df)
