from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ActuatorCreate(BaseModel):
    greenhouse_id: str
    type: str
    value: float
    is_active: bool = Field(True, description="Etat d'un actionneur")

class ActuatorUpdate(BaseModel):
    value: Optional[float] = None
    is_active: Optional[bool] = None

class ActuatorResponse(BaseModel):
    id: str
    greenhouse_id: str
    type: str
    value: float
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True