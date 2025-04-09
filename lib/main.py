from lib.download_extract_data import process_data_from_google_drive
from lib.create_db import create_database
from lib.load_to_db import load_all
from lib.trial_conversion_check import mark_converted_trials

if __name__ == "__main__":
    print("📥 Download files from google drive...")
    process_data_from_google_drive()

    print("▶️ Creating DB...")
    create_database()

    print("📥 Download files into DB...")
    load_all()

    print("🔁 Conversion check...")
    mark_converted_trials()

    print("✅ Tadam! Done!")