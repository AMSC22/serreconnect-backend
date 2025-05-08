from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import get_local_time

class SettingsModel(BaseModel):
    """Modèle MongoDB pour les paramètres dans SmartGreenhouse"""
    id: str = Field(..., description="ID des paramètres")
    user_id: Optional[str] = Field(..., description="ID de l'utilisateur associé")
    greenhouse_id: Optional[str] = Field(..., description="ID de la serre associée")
    temperature_min: Optional[float] = Field(None, description="Seuil minimum de température (°C)")
    temperature_max: Optional[float] = Field(None, description="Seuil maximum de température (°C)")
    humidity_min: Optional[float] = Field(None, description="Seuil minimum d'humidité (%)")
    humidity_max: Optional[float] = Field(None, description="Seuil maximum d'humidité (%)")
    light_level_min: Optional[float] = Field(None, description="Seuil minimum de luminosité (lux)")
    light_level_max: Optional[float] = Field(None, description="Seuil maximum de luminosité (lux)")
    soil_moisture_min: Optional[float] = Field(None, description="Seuil minimum d'humidité du sol (%)")
    soil_moisture_max: Optional[float] = Field(None, description="Seuil maximum d'humidité du sol (%)")
    ph_level_min: Optional[float] = Field(None, description="Seuil minimum de pH")
    ph_level_max: Optional[float] = Field(None, description="Seuil maximum de pH")
    co2_level_max: Optional[float] = Field(None, description="Seuil maximum de CO2 (ppm)")
    notify_by_email: bool = Field(default=False, description="Activer les notifications par email")
    measurement_frequency: Optional[int] = Field(None, description="Fréquence de mesure des capteurs (minutes)")
    is_default: bool = False 
    created_at: datetime = Field(default_factory=get_local_time, description="Date de création")
    updated_at: datetime = Field(default_factory=get_local_time, description="Date de mise à jour")

    class Config:
        collection_name = "settings"