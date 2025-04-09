import pandas as pd
import mysql.connector
import re


def calculate_revenue_from_subscription_data(df):
    df['calculated_revenue'] = df.apply(calculate_revenue, axis=1)
    return df


def calculate_revenue(row):
    """
    Calculate revenue based on the subscription data.
    If refund is 'Yes', return a negative value.
    If 'trial' or 'Free Trial' is present, return 0.
    If 'Weekly' and 'no trial' are present, return 9.99.
    Else, extract the price from the subscription name.

    Parameters:
        row (pd.Series): A row of the DataFrame.

    Returns:
        float: The calculated revenue.
    """
    if 'trial' in row['subscription_name'].lower() or 'Free Trial' in row['intro_price_type']:
        return 0.0
    if row['refund'] == 'Yes':
        match = re.search(r'(\d+\.\d{2})', row['subscription_name'])
        if match:
            return -float(match.group(1))
        return 0.0
    match = re.search(r'(\d+\.\d{2})', row['subscription_name'])
    if match:
        price = float(match.group(1))
        if 'Weekly' in row['subscription_name'] and 'no trial' in row['subscription_name']:
            return 9.99
        return price
    return 0.0


def get_subscription_data_from_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="test",
        password="test",
        database="itunes_db"
    )
    query = "SELECT * FROM subscriptions"
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(rows)
    return df


def export_revenue_data_to_db(df):
    conn = mysql.connector.connect(
        host="localhost",
        user="test",
        password="test",
        database="itunes_db"
    )
    cursor = conn.cursor()

    for index, row in df.iterrows():
        cursor.execute("""
            UPDATE subscriptions
            SET calculated_revenue = %s
            WHERE id = %s
        """, (row['calculated_revenue'], row['id']))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    df = get_subscription_data_from_db()
    df_with_revenue = calculate_revenue_from_subscription_data(df)
    export_revenue_data_to_db(df_with_revenue)

    print("Revenue calculations and database update completed.")
