# database/connection.py
import os
from dotenv import load_dotenv
import psycopg2
 
load_dotenv(".env")
 
def get_database_connection():
 
    dbname = os.environ.get('DB_NAME')
    user = os.environ.get('DB_USER')
    password = os.environ.get('DB_PASSWORD')
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
 
    return psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )


def execute_query(query, params=None):
    try:
        with get_database_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    return cur.fetchall()
                else:
                    conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#Same connection as above, but exclusively used for queries that start with "WITH'"
def execute_search_query(query, params=None):
    with get_database_connection() as conn:
        with conn.cursor() as cur:
            # breakpoint()
            cur.execute(query, params)

            if query.strip().upper().startswith("SELECT") or query.strip().upper().startswith("WITH") :
                return cur.fetchall()
            else:
                conn.commit()
                return None