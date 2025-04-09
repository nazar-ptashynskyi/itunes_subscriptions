import mysql.connector

def create_database():
    root_conn = mysql.connector.connect(
        host="localhost",
        user="test",
        password="test"
    )
    root_cursor = root_conn.cursor()
    root_cursor.execute("CREATE DATABASE IF NOT EXISTS itunes_db")
    root_conn.close()

    conn = mysql.connector.connect(
        host="localhost",
        user="test",
        password="test",
        database="itunes_db"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            event_date DATE,
            app_name TEXT,
            app_apple_id TEXT,
            subscription_name TEXT,
            subscription_apple_id TEXT,
            subscription_group_id TEXT,
            subscription_duration TEXT,
            intro_price_type TEXT,
            intro_price_duration TEXT,
            marketing_opt_in_duration TEXT,
            customer_price FLOAT,
            customer_currency TEXT,
            currency_rate_found BOOLEAN,
            developer_proceeds FLOAT,
            proceeds_currency TEXT,
            preserved_pricing TEXT,
            proceeds_reason TEXT,
            client TEXT,
            device TEXT,
            country TEXT,
            subscriber_id TEXT,
            subscriber_id_reset TEXT,
            refund TEXT,
            purchase_date DATE,
            units INT,
            usd_price FLOAT,
            usd_proceeds FLOAT,
            is_trial TINYINT(1),
            is_converted_from_trial TINYINT(1),
            revenue DECIMAL(10, 2) DEFAULT 0.0
        );
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()