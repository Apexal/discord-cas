import psycopg2.pool
import psycopg2.extras
import os

conn_pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=10, cursor_factory=psycopg2.extras.DictCursor, dsn=os.environ.get(
    'DATABASE_URL'))

def fetch_user(conn, rcs_id: str):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE rcs_id=%s LIMIT 1", (rcs_id,))
        return cursor.fetchone()
    
def fetch_clients(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM clients ORDER BY created_at")
        return cursor.fetchall()

def fetch_client(conn, client_id: str):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM clients WHERE client_id=%s LIMIT 1", (client_id,))
        return cursor.fetchone()