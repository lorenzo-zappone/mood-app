import sqlite3
from datetime import date

DB_NAME = "mood_logs.db"

def create_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            log_date DATE NOT NULL,
            mood TEXT NOT NULL,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_mood_log(user_email, mood, note):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO mood_logs (user_email, log_date, mood, note)
        VALUES (?, ?, ?, ?)
    ''', (user_email, date.today(), mood, note))
    conn.commit()
    conn.close()

def get_mood_logs(user_email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT log_date, mood, note
        FROM mood_logs
        WHERE user_email = ?
        ORDER BY log_date DESC
    ''', (user_email,))
    rows = cursor.fetchall()
    conn.close()
    return rows
