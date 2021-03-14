from typing import Dict
import psycopg2.pool
import psycopg2.extras
import os

conn_pool = psycopg2.pool.SimpleConnectionPool(minconn=1, maxconn=10, cursor_factory=psycopg2.extras.RealDictCursor, dsn=os.environ.get(
    'DATABASE_URL'))

def fetch_user(conn, rcs_id: str):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE rcs_id=%s LIMIT 1", (rcs_id,))
        return cursor.fetchone()

def upsert_user(conn, rcs_id: str, user_dict: Dict):
    with conn.cursor() as cursor:
        # Check if users exists
        cursor.execute("SELECT * FROM users WHERE rcs_id=%s", (rcs_id,))
        if cursor.fetchone():
            # Update user
            raise NotImplementedError()
        else:
            # New user
            cursor.execute("""
                INSERT INTO users (rcs_id, first_name, last_name, graduation_year)
                VALUES (%(rcs_id)s, %(first_name)s, %(last_name)s, %(graduation_year)s)
            """, {"rcs_id": rcs_id, **user_dict})
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE rcs_id=%s", (rcs_id,))
        return cursor.fetchone()

def delete_user(conn, rcs_id: str):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE rcs_id=%s", (rcs_id,))
        conn.commit()

def fetch_clients(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM clients ORDER BY created_at")
        return cursor.fetchall()

def fetch_client(conn, client_id: str):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM clients WHERE client_id=%s LIMIT 1", (client_id,))
        return cursor.fetchone()

def add_client(conn, form: Dict):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO clients (
                client_id,
                name,
                welcome_message,
                discord_server_id,
                discord_rpi_role_id,
                is_public
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            );
        """, (
            form['client_id'],
            form['name'],
            form['welcome_message'],
            form['discord_server_id'],
            form['discord_rpi_role_id'],
            form.get('is_public') == 'on'
        ))
        conn.commit()

        cursor.execute("SELECT * FROM clients WHERE client_id=%s", (form['client_id'],))
        return cursor.fetchone()

def delete_client(conn, client_id: str):
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM clients WHERE client_id=%s", (client_id,))
        conn.commit()