from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import convert_to_local_time

class SessionBase(BaseModel):
    """Schéma de base pour Session"""
    user_id: str = Field(..., description="ID de l'utilisateur")
    session_id: str = Field(..., description="Identifiant unique de la session")
    is_active: bool = Field(default=True, description="Statut de la session")

class SessionCreate(SessionBase):
    """Schéma pour la création d'une session"""
    pass

class SessionUpdate(BaseModel):
    """Schéma pour la mise à jour d'une session"""
    is_active: Optional[bool] = Field(None, description="Statut de la session")

class SessionResponse(SessionBase):
    """Schéma pour la réponse d'une session"""
    id: str = Field(..., description="Identifiant unique")
    last_activity: datetime = Field(..., description="Dernière activité")
    created_at: datetime = Field(..., description="Date de création")

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = obj.dict()
        data["created_at"] = convert_to_local_time(data["created_at"])
        data["last_activity"] = convert_to_local_time(data["last_activity"])
        return cls(**data)