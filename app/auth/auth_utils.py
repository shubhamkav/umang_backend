from dotenv import load_dotenv
load_dotenv()  # MUST be at top

import hashlib
import os
from datetime import datetime, timedelta
from jose import jwt, JWTError

# ================= CONFIG =================
SECRET_KEY = "UMANG_SUPER_SECRET_KEY_CHANGE_THIS"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# ================= HELPERS =================
def get_admin_username() -> str:
    return os.getenv("ADMIN_USERNAME")


def get_admin_password_hash() -> str:
    return os.getenv("ADMIN_PASSWORD_HASH")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str) -> bool:
    """
    Always compares against the CURRENT value from .env
    """
    stored_hash = get_admin_password_hash()
    if not stored_hash:
        return False
    return hash_password(plain_password) == stored_hash


# ================= JWT =================
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
