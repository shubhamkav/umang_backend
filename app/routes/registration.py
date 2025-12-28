from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.db import get_db
from app.models.participant import Participant
from app.models.registration import Registration
from app.models.event import Event
from app.models.team_member import TeamMember
from app.schemas.registration import RegistrationRequest
from app.utils.whatsapp_utils import send_whatsapp_confirmation

router = APIRouter(prefix="/register", tags=["Registration"])

TEAM_SIZE_MAP = {
    "Cricket": 11,
    "Volleyball": 6,
    "Kabaddi": 7,
    "Relay 4x100 m": 4,
    "Relay 4x400 m": 4
}


@router.post("/")
def register_event(payload: RegistrationRequest, db: Session = Depends(get_db)):

    # ==========================
    # 1️⃣ EVENT
    # ==========================
    event = db.query(Event).filter(Event.id == payload.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # ==========================
    # 2️⃣ PARTICIPANT
    # ==========================
    participant = db.query(Participant).filter(
        Participant.roll_number == payload.roll_number
    ).first()

    if not participant:
        participant = Participant(
            name=payload.name.strip(),
            roll_number=payload.roll_number.strip(),
            department=payload.department,
            year=payload.year,
            gender=payload.gender,
            email=payload.email,
            phone=payload.phone
        )
        db.add(participant)
        try:
            db.commit()
            db.refresh(participant)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Participant already exists"
            )

    # ==========================
    # 3️⃣ MODE (🔥 TRUST FRONTEND)
    # ==========================
    mode = payload.mode  # solo | pair | team
    team_members = payload.team_members or []

    # ==========================
    # 4️⃣ VALIDATION
    # ==========================
    if mode == "team":
        if not payload.team_name:
            raise HTTPException(status_code=400, detail="Team name required")

        required = TEAM_SIZE_MAP.get(event.name)
        if required and len(team_members) != required:
            raise HTTPException(
                status_code=400,
                detail=f"{event.name} requires exactly {required} players"
            )

    elif mode == "pair":
        if len(team_members) != 2:
            raise HTTPException(
                status_code=400,
                detail="Pair registration requires exactly 2 players"
            )

    elif mode == "solo":
        if team_members:
            raise HTTPException(
                status_code=400,
                detail="Solo registration cannot have team members"
            )

    for m in team_members:
        if not m.roll_number or len(m.roll_number) > 15:
            raise HTTPException(
                status_code=400,
                detail="Invalid roll number for team member"
            )

    # ==========================
    # 5️⃣ CREATE REGISTRATION (DB ENFORCES UNIQUENESS)
    # ==========================
    registration = Registration(
        participant_id=participant.id,
        event_id=event.id,
        team_name=payload.team_name,
        mode=mode
    )

    db.add(registration)

    try:
        db.commit()
        db.refresh(registration)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail=f"You are already registered for this event as {mode}"
        )

    # ==========================
    # 6️⃣ SAVE TEAM / PAIR MEMBERS
    # ==========================
    for m in team_members:
        db.add(TeamMember(
            registration_id=registration.id,
            member_name=m.name.strip(),
            member_roll=m.roll_number.strip()
        ))

    db.commit()

    # ==========================
    # 7️⃣ WHATSAPP (NON-BLOCKING)
    # ==========================
    try:
        send_whatsapp_confirmation(
            phone=participant.phone,
            name=participant.name,
            event=event.name,
            category=event.category,
            team=payload.team_name
        )
    except Exception:
        pass

    # ==========================
    # 8️⃣ RESPONSE
    # ==========================
    return {
        "message": "Registration successful",
        "event": event.name,
        "mode": mode,
        "team": payload.team_name,
        "players": len(team_members) if team_members else 1
    }
