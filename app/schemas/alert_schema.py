from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import convert_to_local_time

class AlertBase(BaseModel):
    """Schéma de base pour Alert"""
    greenhouse_id: str = Field(..., description="ID de la serre associée")
    type: str = Field(..., description="Type d'alerte (ex. temperature_high, humidity_low)")
    value: float = Field(..., description="Valeur du capteur ayant déclenché l'alerte")
    message: str = Field(..., description="Message descriptif de l'alerte")
    is_resolved: bool = Field(default=False, description="Statut de résolution")

class AlertCreate(AlertBase):
    """Schéma pour la création d'une alerte"""
    pass

class AlertUpdate(BaseModel):
    """Schéma pour la mise à jour d'une alerte"""
    type: Optional[str] = Field(None, description="Type d'alerte")
    value: Optional[float] = Field(None, description="Valeur du capteur")
    message: Optional[str] = Field(None, description="Message descriptif")
    is_resolved: Optional[bool] = Field(None, description="Statut de résolution")

class AlertResponse(AlertBase):
    """Schéma pour la réponse d'une alerte"""
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