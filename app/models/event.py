from sqlalchemy import Column, Integer, String
from app.database.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    category = Column(String(20))
    participation_type = Column(String(20))
