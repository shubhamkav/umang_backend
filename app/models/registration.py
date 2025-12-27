from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.sql import func
from app.database.db import Base

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True)
    participant_id = Column(Integer, ForeignKey("participants.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    team_name = Column(String(100), nullable=True)

    # ✅ Column already exists in DB
    registered_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("participant_id", "event_id"),
    )
