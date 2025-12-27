from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.participant import Participant
from app.models.registration import Registration
from app.models.event import Event
from app.schemas.registration import RegistrationRequest

from app.utils.whatsapp_utils import send_whatsapp_confirmation  # 👈 STEP 7

router = APIRouter(prefix="/register", tags=["Registration"])


@router.post("/")
def register_event(payload: RegistrationRequest, db: Session = Depends(get_db)):
    # 1️⃣ Validate event
    event = db.query(Event).filter(Event.id == payload.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # 2️⃣ Find or create participant
    participant = db.query(Participant).filter(
        (Participant.roll_number == payload.roll_number) |
        (Participant.email == payload.email)
    ).first()

    if not participant:
        participant = Participant(
            name=payload.name,
            roll_number=payload.roll_number,
            department=payload.department,
            year=payload.year,
            email=payload.email,
            phone=payload.phone
        )
        db.add(participant)
        db.commit()
        db.refresh(participant)

    # 3️⃣ Team validation
    if event.participation_type == "team" and not payload.team_name:
        raise HTTPException(status_code=400, detail="Team name required")

    # 4️⃣ Create registration
    registration = Registration(
        participant_id=participant.id,
        event_id=event.id,
        team_name=payload.team_name
    )

    db.add(registration)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Already registered")

    # 5️⃣ WHATSAPP CONFIRMATION (STEP 7) ✅
    try:
        send_whatsapp_confirmation(
            phone=participant.phone,
            name=participant.name,
            event=event.name,
            category=event.category,
            team=registration.team_name
        )
    except Exception as e:
        # ⚠️ Do NOT break registration
        print("WhatsApp notification failed:", e)

    # 6️⃣ Final response
    return {
        "message": "Registration successful"
    }
