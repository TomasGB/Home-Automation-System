import sqlite3
from app.config import Config

DB_PATH = Config.DB_PATH

class UserModel:
    @staticmethod
    def create_table():
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT DEFAULT 'user'
                )
            """)

    @staticmethod
    def find_by_username(username):
        with sqlite3.connect(DB_PATH) as conn:
            return conn.execute("""
                SELECT id, username, password_hash, role
                FROM users WHERE username=?
            """, (username, )).fetchone()

    @staticmethod
    def create_user(username, password_hash, role="user"):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            """, (username, password_hash, role))
