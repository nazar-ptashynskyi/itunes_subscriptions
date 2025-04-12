from lib.create_db import create_database
from lib.download_extract_data import process_data_from_google_drive
from lib.trial_conversion_check import mark_converted_trials
from lib.currency_rates import print_unsupported_currency_summary

if __name__ == "__main__":
    print("▶️ Creating DB...")
    create_database()

    print("📥 Download files from Google Drive & load to DB...")
    process_data_from_google_drive()

    print_unsupported_currency_summary()

    print("🔁 Conversion check...")
    mark_converted_trials()

    print("✅ Tadam! Done!")
