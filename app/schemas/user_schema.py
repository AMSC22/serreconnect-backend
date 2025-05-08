from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from app.utils.time_utils import convert_to_local_time

class UserBase(BaseModel):
    """Schéma de base pour User"""
    username: str = Field(..., description="Nom d'utilisateur")
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    is_admin: bool = Field(default=False, description="Statut administrateur")
    is_active: bool = Field(default=True, description="Statut d'activation")

class UserCreate(UserBase):
    """Schéma pour la création d'un User"""
    password: str = Field(..., description="Mot de passe en clair")

class UserUpdate(BaseModel):
    """Schéma pour la mise à jour d'un User"""
    username: Optional[str] = Field(None, description="Nom d'utilisateur")
    email: Optional[EmailStr] = Field(None, description="Email de l'utilisateur")
    password: Optional[str] = Field(None, description="Mot de passe en clair")
    is_admin: Optional[bool] = Field(None, description="Statut administrateur")
    is_active: Optional[bool] = Field(None, description="Statut d'activation")
    reset_token: Optional[str] = Field(None, description="Token de réinitialisation de mot de passe")

class UserResponse(UserBase):
    """Schéma pour la réponse d'un User"""
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