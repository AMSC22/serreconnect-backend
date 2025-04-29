from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import convert_to_local_time

class GreenhouseBase(BaseModel):
    """Schéma de base pour Greenhouse"""
    name: str = Field(..., description="Nom de la serre")
    description: Optional[str] = Field(None, description="Description de la serre")
    user_id: str = Field(..., description="ID de l'utilisateur propriétaire")
    temperature: Optional[float] = Field(None, description="Température actuelle (°C)")
    humidity: Optional[float] = Field(None, description="Humidité actuelle (%)")
    light_level: Optional[float] = Field(None, description="Niveau de luminosité (lux)")
    soil_moisture: Optional[float] = Field(None, description="Humidité du sol (%)")
    ph_level: Optional[float] = Field(None, description="Niveau de pH (0-14)")
    co2_level: Optional[float] = Field(None, description="Niveau de CO2 (ppm)")
    temperature_threshold: Optional[float] = Field(None, description="Seuil de température pour les alertes (°C)")
    humidity_threshold: Optional[float] = Field(None, description="Seuil d'humidité pour les alertes (%)")
    ph_level_min: Optional[float] = Field(None, description="Seuil minimum de pH pour les alertes")
    ph_level_max: Optional[float] = Field(None, description="Seuil maximum de pH pour les alertes")
    co2_level_max: Optional[float] = Field(None, description="Seuil maximum de CO2 pour les alertes (ppm)")
    is_active: bool = Field(default=True, description="Statut d'activation")

class GreenhouseCreate(GreenhouseBase):
    """Schéma pour la création d'une serre"""
    pass

class GreenhouseUpdate(BaseModel):
    """Schéma pour la mise à jour d'une serre"""
    name: Optional[str] = Field(None, description="Nom de la serre")
    description: Optional[str] = Field(None, description="Description de la serre")
    temperature: Optional[float] = Field(None, description="Température actuelle (°C)")
    humidity: Optional[float] = Field(None, description="Humidité actuelle (%)")
    light_level: Optional[float] = Field(None, description="Niveau de luminosité (lux)")
    soil_moisture: Optional[float] = Field(None, description="Humidité du sol (%)")
    ph_level: Optional[float] = Field(None, description="Niveau de pH (0-14)")
    co2_level: Optional[float] = Field(None, description="Niveau de CO2 (ppm)")
    temperature_threshold: Optional[float] = Field(None, description="Seuil de température pour les alertes (°C)")
    humidity_threshold: Optional[float] = Field(None, description="Seuil d'humidité pour les alertes (%)")
    ph_level_min: Optional[float] = Field(None, description="Seuil minimum de pH pour les alertes")
    ph_level_max: Optional[float] = Field(None, description="Seuil maximum de pH pour les alertes")
    co2_level_max: Optional[float] = Field(None, description="Seuil maximum de CO2 pour les alertes (ppm)")
    is_active: Optional[bool] = Field(None, description="Statut d'activation")

class GreenhouseResponse(GreenhouseBase):
    """Schéma pour la réponse d'une serre"""
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