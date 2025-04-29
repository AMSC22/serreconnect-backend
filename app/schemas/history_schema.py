from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import convert_to_local_time

class HistoryBase(BaseModel):
    """Schéma de base pour History"""
    greenhouse_id: str = Field(..., description="ID de la serre associée")
    temperature: Optional[float] = Field(None, description="Température (°C)")
    humidity: Optional[float] = Field(None, description="Humidité (%)")
    light_level: Optional[float] = Field(None, description="Niveau de luminosité (lux)")
    soil_moisture: Optional[float] = Field(None, description="Humidité du sol (%)")
    ph_level: Optional[float] = Field(None, description="Niveau de pH (0-14)")
    co2_level: Optional[float] = Field(None, description="Niveau de CO2 (ppm)")

class HistoryCreate(HistoryBase):
    """Schéma pour la création d'une entrée historique"""
    pass

class HistoryResponse(HistoryBase):
    """Schéma pour la réponse d'une entrée historique"""
    id: str = Field(..., description="Identifiant unique")
    recorded_at: datetime = Field(..., description="Date d'enregistrement")

    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        data = obj.dict()
        data["created_at"] = convert_to_local_time(data["created_at"])
        data["updated_at"] = convert_to_local_time(data["updated_at"])
        return cls(**data)