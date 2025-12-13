import bcrypt
import jwt
import datetime
from app.models.user_model import UserModel
from app.config import Config


class AuthService:

    @staticmethod
    def login(username, password):
        user = UserModel.find_by_username(username)
        if not user:
            return None

        # user returns a tuple from SQLite → convert to named variables
        user_id, db_username, password_hash, role = user

        if not password_hash or not isinstance(password_hash, str):
            # Stored password is invalid
            return None

        try:
            if not bcrypt.checkpw(password.encode(), password_hash.encode()):
                return None
        except ValueError:
            # Happens when stored password is NOT a bcrypt hash
            return None
        except Exception:
            return None

        # Generate JWT
        payload = {
            "user_id": user_id,
            "username": db_username,
            "role": role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=5)
        }

        token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")

        if isinstance(token, bytes):
            token = token.decode()

        return token


    @staticmethod
    def register(username, password, role="user"):
        """Creates a new user with bcrypt password hashing."""
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        UserModel.create_user(username, hashed, role)
        return True
    
    @staticmethod
    def verify_token(token):
        try:
            decoded = jwt.decode(
                token,
                Config.JWT_SECRET,
                algorithms=["HS256"]
            )
            return decoded
        except Exception:
            return None

