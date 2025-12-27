from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# App routes
from app.routes import sports, cultural, registration, admin

# Auth routes
from app.auth import admin_auth

app = FastAPI(title="College Event Portal API")

# =========================
# CORS CONFIG
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # OK for college project
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ROUTERS
# =========================
app.include_router(sports.router)
app.include_router(cultural.router)
app.include_router(registration.router)
app.include_router(admin.router)
app.include_router(admin_auth.router)   # ✅ AUTH ROUTER (IMPORTANT)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"status": "Backend running successfully"}
