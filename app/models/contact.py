from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from app.database.db import Base
from sqlalchemy.sql import func

class ContactMessage(Base):
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    submitted_at = Column(TIMESTAMP, server_default=func.now())
