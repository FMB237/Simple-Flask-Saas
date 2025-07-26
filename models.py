import sqlite3
from datetime import datetime

DB_NAME = 'users.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Table: users (with role)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    ''')

    # Table: files
    c.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            upload_time DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# ----------------------------
# USER OPERATIONS
# ----------------------------

def get_user(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(username, password_hash, role='user'):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO users (username, password, role) VALUES (?, ?, ?)', (username, password_hash, role))
    conn.commit()
    conn.close()

# ----------------------------
# FILE OPERATIONS
# ----------------------------

def add_file(user_id, filename):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('INSERT INTO files (user_id, filename) VALUES (?, ?)', (user_id, filename))
    conn.commit()
    conn.close()

def get_user_files(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, filename, upload_time FROM files WHERE user_id = ?', (user_id,))
    files = c.fetchall()
    conn.close()
    return files

def get_user_file_count(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM files WHERE user_id = ?', (user_id,))
    count = c.fetchone()[0]
    conn.close()
    return count

def delete_file_record(user_id, file_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('DELETE FROM files WHERE id = ? AND user_id = ?', (file_id, user_id))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT id, username, role FROM users ORDER BY id ASC')
    users = c.fetchall()
    conn.close()
    return users

def update_password(username, new_password_hash):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE users SET password = ? WHERE username = ?', (new_password_hash, username))
    conn.commit()
    conn.close()



