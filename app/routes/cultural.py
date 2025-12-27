from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.event import Event

router = APIRouter(prefix="/cultural")

@router.get("/events")
def get_cultural_events(db: Session = Depends(get_db)):
    return db.query(Event).filter(Event.category == "cultural").all()
