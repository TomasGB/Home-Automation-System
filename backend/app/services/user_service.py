import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from ..config import Config

DB_PATH = Config.DB_PATH

class UserService:
    def __init__(self):
        self.db_path = DB_PATH

    def create_user(self, username, password, role="user"):
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute(
                    """
                    INSERT INTO users (username, password_hash, role)
                    VALUES (?, ?, ?)
                    """,
                    (username, generate_password_hash(password), role)
                )
            return True
        except Exception as e:
            print("Failed to create user:", e)
            return False

    def authenticate_user(self, username, password):
        with sqlite3.connect(self.db_path) as conn:
            user = conn.execute(
                "SELECT id, password_hash, role FROM users WHERE username = ?",
                (username,)
            ).fetchone()

            if not user:
                return None

            user_id, password_hash, role = user

            if check_password_hash(password_hash, password):
                return {"id": user_id, "username": username, "role": role}
            else:
                return None

    def user_exists(self, username):
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT id FROM users WHERE username = ?",
                (username,)
            ).fetchone()
            return row is not None
