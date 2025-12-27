from pydantic import BaseModel
from typing import Optional

class RegistrationRequest(BaseModel):
    name: str
    roll_number: str
    department: str
    year: str
    email: str
    phone: str
    event_id: int
    team_name: Optional[str] = None
