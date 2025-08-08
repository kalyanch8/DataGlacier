from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class ContactRequest(Base):
    __tablename__ = "contact_requests"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String(100), index=True)
    service = Column(String(100))
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
