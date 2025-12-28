from fastapi import APIRouter, Depends, Header, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from collections import defaultdict
import csv, io

from app.database.db import get_db
from app.models.registration import Registration
from app.models.participant import Participant
from app.models.event import Event
from app.models.team_member import TeamMember
from app.auth.auth_utils import verify_token

router = APIRouter(prefix="/admin", tags=["Admin"])


# ================= AUTH =================
def check_admin_auth(authorization: str | None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = authorization.split(" ", 1)[1].strip()
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ================= GET REGISTRATIONS =================
@router.get("/registrations")
def get_all_registrations(
    gender: str = Query(default="all"),
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db)
):
    check_admin_auth(authorization)

    query = (
        db.query(
            Registration.id.label("registration_id"),
            Registration.team_name,
            Registration.registered_at,

            Participant.name,
            Participant.roll_number,
            Participant.department,
            Participant.year,
            Participant.gender,
            Participant.email,
            Participant.phone,              # ✅ ADDED

            Event.name.label("event"),
            Event.category,
        )
        .select_from(Registration)
        .join(Participant, Participant.id == Registration.participant_id)
        .join(Event, Event.id == Registration.event_id)
    )

    if gender != "all":
        query = query.filter(Participant.gender == gender)

    rows = query.order_by(Registration.registered_at.desc()).all()

    # -------- TEAM MEMBERS --------
    member_rows = db.query(
        TeamMember.registration_id,
        TeamMember.member_name,
        TeamMember.member_roll
    ).all()

    team_map = defaultdict(list)
    for m in member_rows:
        team_map[m.registration_id].append({
            "member_name": m.member_name,
            "member_roll": m.member_roll
        })

    response = []
    for r in rows:
        response.append({
            "name": r.name,
            "roll_number": r.roll_number,
            "department": r.department,
            "year": r.year,
            "gender": r.gender,
            "email": r.email,
            "phone": r.phone,              # ✅ ADDED
            "event": r.event,
            "category": r.category,
            "team": r.team_name,
            "time": r.registered_at,
            "players": team_map.get(r.registration_id, [])
        })

    return response


# ================= EXPORT CSV =================
@router.get("/export")
def export_registrations(
    category: str = Query(...),
    event_name: str = Query(...),
    gender: str = Query(default="all"),
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db)
):
    check_admin_auth(authorization)

    query = (
        db.query(
            Registration.id.label("registration_id"),
            Registration.team_name,
            Registration.registered_at,

            Participant.name,
            Participant.roll_number,
            Participant.department,
            Participant.year,
            Participant.gender,
            Participant.email,
            Participant.phone,             # ✅ ADDED

            Event.name.label("event"),
            Event.category,
        )
        .select_from(Registration)
        .join(Participant, Participant.id == Registration.participant_id)
        .join(Event, Event.id == Registration.event_id)
        .filter(Event.category == category)
        .filter(Event.name == event_name)
    )

    if gender != "all":
        query = query.filter(Participant.gender == gender)

    rows = query.order_by(Registration.registered_at.asc()).all()

    # -------- TEAM MEMBERS --------
    member_rows = db.query(
        TeamMember.registration_id,
        TeamMember.member_name,
        TeamMember.member_roll
    ).all()

    team_map = defaultdict(list)
    for m in member_rows:
        team_map[m.registration_id].append(
            f"{m.member_name} ({m.member_roll})"
        )

    # -------- CSV --------
    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "Name",
        "Roll Number",
        "Phone Number",          # ✅ ADDED
        "Department",
        "Year",
        "Gender",
        "Email",
        "Event",
        "Category",
        "Team Name",
        "Team Members",
        "Registered At"
    ])

    for r in rows:
        writer.writerow([
            r.name,
            r.roll_number,
            r.phone,              # ✅ ADDED
            r.department,
            r.year,
            r.gender,
            r.email,
            r.event,
            r.category,
            r.team_name or "-",
            ", ".join(team_map.get(r.registration_id, [])),
            r.registered_at.strftime("%Y-%m-%d %H:%M:%S")
        ])

    output.seek(0)

    filename = f"{event_name}_{category}_{gender}.csv"

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
