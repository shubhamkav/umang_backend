from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class TeamMemberSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    roll_number: str = Field(..., min_length=1, max_length=15)


class RegistrationRequest(BaseModel):
    # ================= BASIC DETAILS =================
    name: str = Field(..., min_length=1, max_length=15)
    roll_number: str = Field(..., min_length=1, max_length=15)
    department: str
    year: str
    gender: Literal["male", "female"]
    email: Optional[str] = None
    phone: Optional[str] = None

    # ================= EVENT =================
    event_id: int

    # ================= MODE (🔥 REQUIRED) =================
    mode: Literal["solo", "pair", "team"]

    # ================= OPTIONAL =================
    team_name: Optional[str] = None
    team_members: Optional[List[TeamMemberSchema]] = None
