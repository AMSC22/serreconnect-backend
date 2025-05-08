from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import convert_to_local_time

class BadgeBase(BaseModel):
    """Schéma de base pour Badge"""
    name: str = Field(..., description="Nom du badge")
    user_id: str = Field(..., description="ID de l'utilisateur associé")
    greenhouse_id: str = Field(..., description="ID de la serre associée")

class BadgeCreate(BadgeBase):
    """Schéma pour la création d'un Badge"""
    pass

class BadgeUpdate(BaseModel):
    """Schéma pour la mise à jour d'un Badge"""
    name: Optional[str] = Field(None, description="Nom du badge")
    user_id: Optional[str] = Field(None, description="ID de l'utilisateur associé")
    greenhouse_id: str = Field(..., description="ID de la serre associée")

class BadgeResponse(BadgeBase):
    """Schéma pour la réponse d'un Badge"""
    id: str = Field(..., description="Identifiant unique")
    created_at: datetime = Field(..., description="Date de création")
    updated_at: datetime = Field(..., description="Date de mise à jour")

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = obj.dict()
        data["created_at"] = convert_to_local_time(data["created_at"])
        data["updated_at"] = convert_to_local_time(data["updated_at"])
        return cls(**data)