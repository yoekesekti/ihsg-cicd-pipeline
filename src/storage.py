
import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


CONTAINER_NAME = "ihsg-data"
BLOB_NAME = "ihsg_historical.csv"


def upload_to_azure(file_path):
    # Memastikan file tersedia
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File tidak ditemukan: {file_path}"
        )

    # Mengambil nama Storage Account dari environment variable
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT")

    if not account_name:
        raise ValueError(
            "Environment variable AZURE_STORAGE_ACCOUNT belum diatur."
        )

    # Membuat URL Azure Blob Storage
    account_url = (
        f"https://{account_name}.blob.core.windows.net"
    )

    # Autentikasi menggunakan Azure Credential
    credential = DefaultAzureCredential()

    # Membuat koneksi ke Blob Storage
    blob_service_client = BlobServiceClient(
        account_url=account_url,
        credential=credential
    )

    # Mengakses container
    container_client = blob_service_client.get_container_client(
        CONTAINER_NAME
    )

    # Membuat container jika belum tersedia
    if not container_client.exists():
        container_client.create_container()

    # Mengakses blob tujuan
    blob_client = container_client.get_blob_client(
        BLOB_NAME
    )

    # Mengunggah file CSV
    with open(file_path, "rb") as data:
        blob_client.upload_blob(
            data,
            overwrite=True
        )

    print("Upload ke Azure Blob Storage berhasil.")
    print(f"Container: {CONTAINER_NAME}")
    print(f"Blob: {BLOB_NAME}")


if __name__ == "__main__":
    upload_to_azure("data/ihsg_historical.csv")

