
import pandas as pd
import pytest

from src.validation import validate_data


@pytest.fixture
def sample_data():
    return pd.DataFrame({
        "Date": ["2024-01-02"] * 8,
        "Open": [
            7200, 100, 2000, 15000,
            38000, 17000, 33000, 40
        ],
        "High": [
            7300, 110, 2100, 15100,
            38100, 17100, 33100, 41
        ],
        "Low": [
            7100, 90, 1900, 14900,
            37900, 16900, 32900, 39
        ],
        "Close": [
            7250, 105, 2050, 15050,
            38050, 17050, 33050, 40.5
        ],
        "Adj Close": [
            7250, 105, 2050, 15050,
            38050, 17050, 33050, 40.5
        ],
        "Volume": [100000] * 8,
        "Ticker": [
            "^JKSE", "CL=F", "GC=F", "IDR=X",
            "^DJI", "^HSI", "^N225", "EEM"
        ],
        "Instrument": [
            "JKSE", "CLF", "GCF", "IDRX",
            "DJI", "HSI", "N225", "EEM"
        ]
    })


def test_valid_data(sample_data):
    assert validate_data(sample_data) is True


def test_empty_data(sample_data):
    with pytest.raises(ValueError, match="Dataset kosong"):
        validate_data(sample_data.iloc[0:0])


def test_missing_column(sample_data):
    data = sample_data.drop(columns=["Open"])

    with pytest.raises(ValueError, match="Kolom tidak lengkap"):
        validate_data(data)


def test_duplicate_data(sample_data):
    data = pd.concat(
        [sample_data, sample_data.iloc[[0]]],
        ignore_index=True
    )

    with pytest.raises(ValueError, match="data duplikat"):
        validate_data(data)


def test_invalid_ticker(sample_data):
    data = sample_data.copy()
    data.loc[0, "Ticker"] = "INVALID"

    with pytest.raises(ValueError, match="Daftar ticker tidak sesuai"):
        validate_data(data)


def test_invalid_date(sample_data):
    data = sample_data.copy()
    data.loc[0, "Date"] = "tanggal-salah"

    with pytest.raises(ValueError, match="tanggal yang tidak valid"):
        validate_data(data)


def test_negative_volume(sample_data):
    data = sample_data.copy()
    data.loc[0, "Volume"] = -100

    with pytest.raises(ValueError, match="Volume memiliki nilai negatif"):
        validate_data(data)


def test_negative_wti_price(sample_data):
    data = sample_data.copy()

    data.loc[1, "Open"] = -14
    data.loc[1, "High"] = 13.86
    data.loc[1, "Low"] = -16
    data.loc[1, "Close"] = 10.01
    data.loc[1, "Adj Close"] = -10

    assert validate_data(data) is True
