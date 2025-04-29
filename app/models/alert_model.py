from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import get_local_time

class AlertModel(BaseModel):
    """Modèle MongoDB pour les alertes dans SmartGreenhouse"""
    id: str = Field(..., description="ID de l'alerte")
    greenhouse_id: str = Field(..., description="ID de la serre associée")
    type: str = Field(..., description="Type d'alerte (ex. temperature_high, humidity_low, ph_low, ph_high, co2_high)")
    value: float = Field(..., description="Valeur du capteur ayant déclenché l'alerte")
    message: str = Field(..., description="Message descriptif de l'alerte")
    is_resolved: bool = Field(default=False, description="Statut de résolution")
    created_at: datetime = Field(default_factory=get_local_time, description="Date de création")
    updated_at: datetime = Field(default_factory=get_local_time, description="Date de mise à jour")

    class Config:
        collection_name = "alerts"