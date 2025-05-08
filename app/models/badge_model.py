from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import get_local_time

class BadgeModel(BaseModel):
    """Modèle MongoDB pour les badges RFID dans SmartGreenhouse"""
    id: str = Field(..., description="ID du badge")
    name: str = Field(..., description="Nom du badge (ex. Employé 1)")
    user_id: str = Field(..., description="ID de l'utilisateur associé")
    greenhouse_id: str = Field(..., description="ID de la serre associée")
    created_at: datetime = Field(default_factory=get_local_time, description="Date de création")
    updated_at: datetime = Field(default_factory=get_local_time, description="Date de mise à jour")

    class Config:
        collection_name = "badges"