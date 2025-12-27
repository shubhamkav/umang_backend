from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel

from app.auth.auth_utils import (
    verify_password,
    create_access_token,
    verify_token,
    hash_password,
    get_admin_username,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# SCHEMAS
# =========================
class LoginRequest(BaseModel):
    username: str
    password: str


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


# =========================
# ADMIN LOGIN
# =========================
@router.post("/admin-login")
def admin_login(data: LoginRequest):
    """
    Admin login using username + password from .env
    """
    if data.username != get_admin_username():
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": "admin"})
    return {"access_token": token}


# =========================
# CHANGE ADMIN PASSWORD
# =========================
@router.post("/change-password")
def change_admin_password(
    data: ChangePasswordRequest,
    authorization: str = Header(None)
):
    """
    Change admin password.
    Requires valid JWT token.
    """

    # 1️⃣ Check auth header
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]

    # 2️⃣ Verify token
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")

    # 3️⃣ Verify old password (ALWAYS read from .env dynamically)
    if not verify_password(data.old_password):
        raise HTTPException(status_code=400, detail="Old password incorrect")

    # 4️⃣ Hash new password
    new_hash = hash_password(data.new_password)

    # 5️⃣ Return new hash (manual .env update step)
    return {
        "message": "Password updated successfully",
        "new_password_hash": new_hash
    }
