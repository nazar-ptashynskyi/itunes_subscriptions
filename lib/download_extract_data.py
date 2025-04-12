import os
import requests
import zipfile
import tempfile
import shutil
from lib.load_to_db import load_all

def download_file_from_google_drive(file_id, dest_path):
    URL = f"https://drive.google.com/uc?export=download&id={file_id}"
    session = requests.Session()
    response = session.get(URL, stream=True)

    if response.status_code == 200:
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        print(f"✅ File downloaded to {dest_path}")
    else:
        raise Exception(f"❌ Failed to download file: {response.status_code}")


def extract_zip_file(zip_file_path, extract_to_path):
    os.makedirs(extract_to_path, exist_ok=True)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)
        print(f"✅ Extracted to {extract_to_path}")


def process_data_from_google_drive():
    file_id = '1v3GyOGez_eV3gdwJhHJ5L4K3KZDFu8rM'

    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_file_path = os.path.join(tmp_dir, "subscription_data.zip")
        extract_to_path = os.path.join(tmp_dir, "extracted")

        download_file_from_google_drive(file_id, zip_file_path)
        extract_zip_file(zip_file_path, extract_to_path)

        load_all(data_dir=extract_to_path)

if __name__ == "__main__":
    process_data_from_google_drive()
