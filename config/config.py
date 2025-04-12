import mysql.connector
import os


DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

SERVER_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

# without docker, when run via main.py
# DB_CONFIG = {
#     'host': os.getenv('DB_HOST', 'localhost'),
#     'user': os.getenv('DB_USER', 'you_name'),
#     'password': os.getenv('DB_PASSWORD', 'your_password'),
#     'database': os.getenv('DB_NAME', 'itunes_db')
# }
# SERVER_CONFIG = {
#     'host': os.getenv('DB_HOST', 'localhost'),
#     'user': os.getenv('DB_USER', 'you_name'),
#     'password': os.getenv('DB_PASSWORD', 'your_password')
# }


def get_server_connection():
    db_conf = mysql.connector.connect(
        host=SERVER_CONFIG['host'],
        user=SERVER_CONFIG['user'],
        password=SERVER_CONFIG['password']
    )
    return db_conf


def get_db_connection():
    db_conf = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )
    return db_conf
