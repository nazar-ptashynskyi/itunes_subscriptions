from config.config import get_server_connection, get_db_connection


def create_database():
    server_conn = get_server_connection()
    cursor = server_conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS itunes_db")
    server_conn.commit()
    server_conn.close()

    db_conf = get_db_connection()
    cursor = db_conf.cursor()

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
            revenue DECIMAL(10, 2) DEFAULT 0.0,

            INDEX idx_subscriber_id (subscriber_id(100)),
            INDEX idx_subscription_apple_id (subscription_apple_id(100)),
            INDEX idx_is_trial (is_trial),
            INDEX idx_event_date (event_date)
        );
    """)
    db_conf.commit()
    db_conf.close()


if __name__ == "__main__":
    create_database()
