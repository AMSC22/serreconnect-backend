from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from app.utils.time_utils import get_local_time
from app.utils.constants import VALID_ACTUATOR_TYPES

class ActuatorModel(BaseModel):
    """Modèle MongoDB pour les actionneurs dans SmartGreenhouse"""
    id: str = Field(..., description="ID de l'actionneur")
    type: str = Field(..., description="Type d'actionneur (fan1, fan2, irrigation, etc.)")
    is_active: bool = Field(True, description="Etat d'un actionneur")
    value: float = Field(..., description="Valeur de l'actionneur (0/1 pour booléen, ou numérique)")
    greenhouse_id: str = Field(..., description="ID de la serre associée")
    created_at: datetime = Field(default_factory=get_local_time, description="Date de création")
    updated_at: datetime = Field(default_factory=get_local_time, description="Date de mise à jour")

    @validator("type")
    def validate_type(cls, v):
        if v not in VALID_ACTUATOR_TYPES:
            raise ValueError(f"Le type doit être l'un des suivants : {', '.join(VALID_ACTUATOR_TYPES)}")
        return v

    class Config:
        collection_name = "actuators"