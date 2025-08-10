from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .email_utils import send_contact_email

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan manager for the FastAPI application.
    Handles startup and shutdown events.
    """
    # On startup, create database tables
    models.Base.metadata.create_all(bind=engine)
    yield
    # On shutdown, you could add cleanup code here

app = FastAPI(
    title="DataGlacier Contact API",
    description="An API to handle contact form submissions.",
    version="1.0.0",
    lifespan=lifespan
)

# Dependency to get a DB session for each request.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/contact", response_model=schemas.ContactRequest, tags=["Contact"])
def create_contact(contact: schemas.ContactRequestCreate, db: Session = Depends(get_db)):
    """
    Create a new contact request.

    - Saves the contact information to the database.
    - Sends an email notification.
    """
    db_contact_request = crud.create_contact_request(db=db, contact_request=contact)
    send_contact_email(contact_request=contact)
    return db_contact_request


@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint with a welcome message.
    """
    return {"message": "Welcome to the DataGlacier Contact API"}
