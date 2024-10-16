import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

def create_table(conn):
    """Create a table for user goals and a table for user logins"""
    try:
        c = conn.cursor()
        # Create the 'goals' table
        c.execute('''CREATE TABLE IF NOT EXISTS goals (
                         user_id TEXT PRIMARY KEY,
                         goals TEXT
                     );''')
        # Create the 'users' table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                         user_id TEXT PRIMARY KEY,
                         name TEXT NOT NULL,
                         password TEXT NOT NULL
                     );''')
    except Exception as e:
        print(e)
