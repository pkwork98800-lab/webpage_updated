import sqlite3
import os

# Fix: use an absolute path based on this file's location instead of a
# relative path. Under WSGI (PythonAnywhere, Render, etc.) the process's
# working directory is not guaranteed to be the project folder, so a
# relative 'admin.db' can silently create/read the database in the wrong
# place, causing "no such table" errors even though init_db() ran before.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'admin.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    # Visits table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Submissions table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            message TEXT,
            attachment_path TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Admin table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS admin_config (
            id INTEGER PRIMARY KEY,
            admin_id TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            pass_key TEXT NOT NULL,
            is_first_login INTEGER DEFAULT 1
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
