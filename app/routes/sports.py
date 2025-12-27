from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.event import Event

router = APIRouter(prefix="/sports")

@router.get("/events")
def get_sports_events(db: Session = Depends(get_db)):
    return db.query(Event).filter(Event.category == "sport").all()
