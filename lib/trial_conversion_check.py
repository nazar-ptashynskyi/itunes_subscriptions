import mysql.connector
from datetime import timedelta

def mark_converted_trials():
    conn = mysql.connector.connect(
        host="localhost",
        user="nazar",
        password="753357Test@",
        database="itunes_db"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subscriber_id, subscription_apple_id, event_date
        FROM subscriptions
        WHERE is_trial = 1
    """)
    trials = cursor.fetchall()

    for subscriber_id, subscription_id, trial_date in trials:
        if not subscriber_id or not trial_date:
            continue

        deadline = trial_date + timedelta(days=7)

        cursor.execute("""
            SELECT id FROM subscriptions
            WHERE subscriber_id = %s
              AND subscription_apple_id = %s
              AND is_trial = 0
              AND usd_price > 0
              AND event_date BETWEEN %s AND %s
            LIMIT 1
        """, (subscriber_id, subscription_id, trial_date, deadline))

        row = cursor.fetchone()
        if row:
            converted_id = row[0]
            cursor.execute("""
                UPDATE subscriptions
                SET is_converted_from_trial = 1
                WHERE id = %s
            """, (converted_id,))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    mark_converted_trials()