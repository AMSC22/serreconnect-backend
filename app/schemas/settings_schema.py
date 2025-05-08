from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import convert_to_local_time

class SettingsBase(BaseModel):
    """Schéma de base pour Settings"""
    user_id: Optional[str] = Field(..., description="ID de l'utilisateur associé")
    greenhouse_id: str = Field(..., description="ID de la serre associée")
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

class SettingsCreate(SettingsBase):
    """Schéma pour la création de paramètres"""
    pass

class SettingsUpdate(BaseModel):
    """Schéma pour la mise à jour de paramètres"""
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
    notify_by_email: Optional[bool] = Field(None, description="Activer les notifications par email")
    measurement_frequency: Optional[int] = Field(None, description="Fréquence de mesure des capteurs (minutes)")
    is_default: bool = False 

class SettingsResponse(SettingsBase):
    """Schéma pour la réponse des paramètres"""
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