from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.utils.time_utils import get_local_time

class UserModel(BaseModel):
    """Modèle MongoDB pour les utilisateurs dans SmartGreenhouse"""
    id: str = Field(..., description="ID de l'utilisateur")
    username: str = Field(..., description="Nom d'utilisateur")
    email: str = Field(..., description="Email de l'utilisateur")
    hashed_password: str = Field(..., description="Mot de passe haché")
    is_admin: bool = Field(default=False, description="Statut administrateur")
    is_active: bool = Field(default=True, description="Statut d'activation")
    created_at: datetime = Field(default_factory=get_local_time, description="Date de création")
    updated_at: datetime = Field(default_factory=get_local_time, description="Date de mise à jour")

    class Config:
        collection_name = "users"