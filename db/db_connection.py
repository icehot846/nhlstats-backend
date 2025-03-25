import psycopg2
from db.db_config import DB_CONFIG

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as err:
        print(f"❌ PostgreSQL connection error: {err}")
        raise
