import os
import mysql.connector
import csv
from lib.currency_rates import get_usd_rate
import re


def clean_price(value):
    try:
        return float(value.strip())
    except:
        return 0.0


def calculate_revenue(row):
    try:
        # 1. If it's a trial or free trial, revenue is 0
        if 'trial' in row['Subscription Name'].lower() or 'Free Trial' in row['Introductory Price Type']:
            return 0

        # 2. Extract the price from the Subscription Name (last number)
        match_price = re.search(r'(\d+\.\d{2}|\d+)(?=\s*$)', row['Subscription Name'])
        if match_price:
            price = float(match_price.group(1))
        else:
            return 0

        # 3. Apply refund logic at the end - if refund is "Yes", apply negative sign
        if row['Refund'] == 'Yes':
            price = -price

        return price

    except Exception as e:
        print(f"Error processing row: {row}. Error: {str(e)}")
        return 0


def process_file(file_path, cursor):
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            event_date = row['Event Date']
            currency = row['Customer Currency']

            customer_price = clean_price(row['Customer Price'])
            proceeds = clean_price(row['Developer Proceeds'])

            usd_rate, rate_found = get_usd_rate(event_date, currency)
            usd_price = round(customer_price * usd_rate, 2)
            usd_proceeds = round(proceeds * usd_rate, 2)
            is_trial = 1 if row['Introductory Price Type'] == 'Free Trial' else 0
            purchase_date = row['Purchase Date'] if row['Purchase Date'].strip() else None

            # Calculate revenue based on the row logic
            revenue = calculate_revenue(row)

            cursor.execute("""
                INSERT INTO subscriptions (
                    event_date, app_name, app_apple_id, subscription_name,
                    subscription_apple_id, subscription_group_id, subscription_duration,
                    intro_price_type, intro_price_duration, marketing_opt_in_duration,
                    customer_price, customer_currency, developer_proceeds, proceeds_currency,
                    preserved_pricing, proceeds_reason, client, device, country,
                    subscriber_id, subscriber_id_reset, refund, purchase_date, units,
                    usd_price, usd_proceeds, is_trial, currency_rate_found, revenue
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                )
            """, (
                row['Event Date'], row['App Name'], row['App Apple ID'], row['Subscription Name'],
                row['Subscription Apple ID'], row['Subscription Group ID'], row['Subscription Duration'],
                row['Introductory Price Type'], row['Introductory Price Duration'], row['Marketing Opt-In Duration'],
                customer_price, currency, proceeds, row['Proceeds Currency'],
                row['Preserved Pricing'], row['Proceeds Reason'], row['Client'], row['Device'], row['Country'],
                row['Subscriber ID'], row['Subscriber ID Reset'], row['Refund'], purchase_date, row['Units'],
                usd_price, usd_proceeds, is_trial, rate_found, revenue
            ))


def load_all():
    conn = mysql.connector.connect(
        host="localhost",
        user="test",
        password="test",
        database="itunes_db"
    )
    cursor = conn.cursor()

    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')

    for file in sorted(os.listdir(data_dir)):
        if file.endswith('.txt'):
            process_file(os.path.join(data_dir, file), cursor)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    load_all()
