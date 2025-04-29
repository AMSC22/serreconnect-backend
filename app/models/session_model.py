from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import get_local_time

class SessionModel(BaseModel):
    """Modèle MongoDB pour les sessions utilisateur"""
    id: str = Field(..., description="ID de la session")
    user_id: str = Field(..., description="ID de l'utilisateur")
    session_id: str = Field(..., description="Identifiant unique de la session")
    last_activity: datetime = Field(default_factory=get_local_time, description="Dernière activité")
    created_at: datetime = Field(default_factory=get_local_time, description="Date de création")
    is_active: bool = Field(default=True, description="Statut de la session")

    class Config:
        collection_name = "sessions"