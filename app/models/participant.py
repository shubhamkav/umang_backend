from sqlalchemy import Column, Integer, String
from app.database.db import Base

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    roll_number = Column(String(20), unique=True, nullable=False)
    department = Column(String(50), nullable=False)
    year = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), nullable=False)

    # ✅ NEW FIELD
    gender = Column(String(10), nullable=False)  # male / female
