from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database.db import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)

    registration_id = Column(
        Integer,
        ForeignKey("registrations.id", ondelete="CASCADE"),
        nullable=False
    )

    member_name = Column(String(100), nullable=False)
    member_roll = Column(String(15), nullable=False)

    is_captain = Column(Boolean, default=False)
