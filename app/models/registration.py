from sqlalchemy import Column, Integer, ForeignKey, String, Enum, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.database.db import Base

class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True)
    participant_id = Column(Integer, ForeignKey("participants.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    team_name = Column(String(100), nullable=True)

    mode = Column(
        Enum("solo", "pair", "team", name="registration_mode"),
        nullable=False
    )

    registered_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "participant_id",
            "event_id",
            "mode",
            name="uq_participant_event_mode"
        ),
    )
