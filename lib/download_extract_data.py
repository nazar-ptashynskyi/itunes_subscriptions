import os
import requests
import zipfile


def download_file_from_google_drive(file_id, dest_path):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    URL = f"https://drive.google.com/uc?export=download&id={file_id}"

    session = requests.Session()
    response = session.get(URL, stream=True)

    if response.status_code == 200:
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=128):
                f.write(chunk)
        print(f"File downloaded successfully to {dest_path}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")


def extract_zip_file(zip_file_path, extract_to_path):
    os.makedirs(extract_to_path, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)
        print(f"File extracted to {extract_to_path}")


def process_data_from_google_drive():
    file_id = '1v3GyOGez_eV3gdwJhHJ5L4K3KZDFu8rM'
    zip_file_path = 'data/subscription_data.zip'
    extract_to_path = '../data'

    download_file_from_google_drive(file_id, zip_file_path)

    extract_zip_file(zip_file_path, extract_to_path)

    for filename in os.listdir(extract_to_path):
        file_path = os.path.join(extract_to_path, filename)
        if filename.endswith(".txt"):
            print(f"Processing file: {filename}")
            process_file(file_path)


def process_file(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            print(line.strip())


if __name__ == "__main__":
    process_data_from_google_drive()
