from config.config import get_db_connection

def mark_converted_trials():
    db_conf = get_db_connection()
    cursor = db_conf.cursor()

    try:
        count_query = """
            SELECT COUNT(*) FROM (
                SELECT s1.id AS trial_id
                FROM subscriptions s1
                JOIN subscriptions s2
                  ON s1.subscriber_id = s2.subscriber_id
                 AND s1.subscription_apple_id = s2.subscription_apple_id
                 AND s1.is_trial = 1
                 AND s2.is_trial = 0
                 AND s2.usd_price > 0
                 AND s2.event_date BETWEEN s1.event_date AND DATE_ADD(s1.event_date, INTERVAL 7 DAY)
            ) AS t;
        """
        cursor.execute(count_query)
        result = cursor.fetchone()

        update_query = """
            UPDATE subscriptions AS trial
            JOIN (
                SELECT s1.id AS trial_id, s2.id AS paid_id
                FROM subscriptions s1
                JOIN subscriptions s2
                  ON s1.subscriber_id = s2.subscriber_id
                 AND s1.subscription_apple_id = s2.subscription_apple_id
                 AND s1.is_trial = 1
                 AND s2.is_trial = 0
                 AND s2.usd_price > 0
                 AND s2.event_date BETWEEN s1.event_date AND DATE_ADD(s1.event_date, INTERVAL 7 DAY)
            ) AS matched
            ON trial.id = matched.trial_id
            SET trial.is_converted_from_trial = 1;
        """
        cursor.execute(update_query)
        db_conf.commit()

    except Exception as e:
        print(f"❌ error: {str(e)}")
        db_conf.rollback()
    finally:
        cursor.close()
        db_conf.close()


if __name__ == "__main__":
    mark_converted_trials()
