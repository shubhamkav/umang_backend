from sqlalchemy import Column, Integer, String
from app.database.db import Base

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    roll_number = Column(String(50), unique=True)
    department = Column(String(50))
    year = Column(String(20))
    email = Column(String(100), unique=True)
    phone = Column(String(20))
