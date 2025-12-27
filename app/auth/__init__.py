from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.auth.auth_utils import (
    verify_password,
    create_access_token,
    get_admin_username,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# SCHEMA
# =========================
class LoginRequest(BaseModel):
    username: str
    password: str


# =========================
# ADMIN LOGIN
# =========================
@router.post("/admin-login")
def admin_login(data: LoginRequest):
    """
    Admin login using credentials from .env (dynamic, no caching)
    """

    # 1️⃣ Check username
    if data.username != get_admin_username():
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 2️⃣ Check password (always reads latest hash from .env)
    if not verify_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3️⃣ Create JWT token
    token = create_access_token({"sub": "admin"})

    return {"access_token": token}
