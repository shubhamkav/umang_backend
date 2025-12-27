from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
import csv
import io

from app.database.db import get_db
from app.models.registration import Registration
from app.models.participant import Participant
from app.models.event import Event
from app.auth.auth_utils import verify_token

router = APIRouter(prefix="/admin", tags=["Admin"])


# ======================================================
# 🔐 AUTH CHECK
# ======================================================
def check_admin_auth(authorization: str):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")

    token = authorization.split(" ")[1]
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ======================================================
# 📊 VIEW ALL REGISTRATIONS
# ======================================================
@router.get("/registrations")
def get_all_registrations(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    check_admin_auth(authorization)

    results = (
        db.query(
            Registration.id,
            Participant.name,
            Participant.roll_number,
            Participant.department,
            Participant.year,
            Participant.email,
            Participant.phone,
            Event.name.label("event_name"),
            Event.category,
            Registration.team_name,
            Registration.registered_at
        )
        .join(Participant, Participant.id == Registration.participant_id)
        .join(Event, Event.id == Registration.event_id)
        .order_by(Registration.registered_at.desc())
        .all()
    )

    return [
        {
            "id": r.id,
            "name": r.name,
            "roll_number": r.roll_number,
            "department": r.department,
            "year": r.year,
            "email": r.email,
            "phone": r.phone,
            "event": r.event_name,
            "category": r.category,
            "team": r.team_name,
            "time": r.registered_at
        }
        for r in results
    ]


# ======================================================
# 📥 EXPORT REGISTRATIONS (FINAL FIX)
# ======================================================
@router.get("/export")
def export_registrations(
    category: str,       # ← use as-is
    event_name: str,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    check_admin_auth(authorization)

    clean_event = event_name.strip()

    results = (
        db.query(
            Participant.name,
            Participant.roll_number,
            Participant.department,
            Participant.year,
            Participant.email,
            Participant.phone,
            Registration.team_name,
            Registration.registered_at
        )
        .join(Participant, Participant.id == Registration.participant_id)
        .join(Event, Event.id == Registration.event_id)
        .filter(Event.category == category)  # ✅ FIX
        .filter(Event.name.ilike(f"%{clean_event}%"))
        .order_by(Registration.registered_at.asc())
        .all()
    )

    # CSV GENERATION
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Participant Name",
        "Roll Number",
        "Department",
        "Year",
        "Email",
        "Phone",
        "Team Name",
        "Registered At"
    ])

    for r in results:
        writer.writerow([
            r.name,
            r.roll_number,
            r.department,
            r.year,
            r.email,
            r.phone,
            r.team_name or "Solo",
            r.registered_at
        ])

    output.seek(0)

    filename = f"{event_name}_{category}_registrations.csv"

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
