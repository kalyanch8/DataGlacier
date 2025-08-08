from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ContactRequestBase(BaseModel):
    name: str
    email: str
    service: str
    message: str

class ContactRequestCreate(ContactRequestBase):
    pass

class ContactRequest(ContactRequestBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
