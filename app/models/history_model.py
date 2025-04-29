from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import get_local_time

class HistoryModel(BaseModel):
    """Modèle MongoDB pour les historiques des capteurs dans SmartGreenhouse"""
    id: str = Field(..., description="ID de l'entrée historique")
    greenhouse_id: str = Field(..., description="ID de la serre associée")
    temperature: Optional[float] = Field(None, description="Température (°C)")
    humidity: Optional[float] = Field(None, description="Humidité (%)")
    light_level: Optional[float] = Field(None, description="Niveau de luminosité (lux)")
    soil_moisture: Optional[float] = Field(None, description="Humidité du sol (%)")
    ph_level: Optional[float] = Field(None, description="Niveau de pH (0-14)")
    co2_level: Optional[float] = Field(None, description="Niveau de CO2 (ppm)")
    recorded_at: datetime = Field(default_factory=get_local_time, description="Date d'enregistrement")

    class Config:
        collection_name = "history"