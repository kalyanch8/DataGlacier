from sqlalchemy.orm import Session
from . import models, schemas

def create_contact_request(db: Session, contact_request: schemas.ContactRequestCreate):
    db_contact_request = models.ContactRequest(**contact_request.model_dump())
    db.add(db_contact_request)
    db.commit()
    db.refresh(db_contact_request)
    return db_contact_request
