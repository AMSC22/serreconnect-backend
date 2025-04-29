from typing import Optional, List, Dict
from app.services.base_service import BaseService
from app.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate
from passlib.context import CryptContext
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class UserService(BaseService[UserModel, UserCreate, UserUpdate]):
    """Service pour gérer les opérations liées aux utilisateurs"""

    def __init__(self):
        super().__init__()
        self.repository = UserRepository()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        """Hacher un mot de passe"""
        return self.pwd_context.hash(password)

    async def create(self, data: UserCreate) -> UserModel:
        """Créer un nouvel utilisateur"""
        try:
            # Vérifier l'unicité de l'email
            existing_user = await self.get_by_email(data.email)
            if existing_user:
                raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")
            
            user_data = data.model_dump()
            user_data["hashed_password"] = self.hash_password(user_data.pop("password"))
            result = await self.repository.create(user_data)
            return UserModel(**result)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'utilisateur: {e}")
            raise

    async def get_by_id(self, id: str) -> Optional[UserModel]:
        """Récupérer un utilisateur par son ID"""
        try:
            entity = await self.repository.get_by_id(id)
            return UserModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'utilisateur: {e}")
            raise

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        """Récupérer un utilisateur par son email"""
        try:
            entity = await self.repository.get_by_email(email)
            return UserModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération par email: {e}")
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """Récupérer tous les utilisateurs"""
        try:
            entities = await self.repository.get_all(skip=skip, limit=limit)
            return [UserModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des utilisateurs: {e}")
            raise

    async def count_by_role(self) -> Dict[str, int]:
        """Compter les utilisateurs par rôle"""
        try:
            return await self.repository.count_by_role()
        except Exception as e:
            logger.error(f"Erreur lors du comptage des utilisateurs: {e}")
            raise

    async def search_by_email(self, email: str, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """Rechercher des utilisateurs par email"""
        try:
            entities = await self.repository.search_by_email(email, skip, limit)
            return [UserModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des utilisateurs: {e}")
            raise

    async def update(self, id: str, data: UserUpdate) -> Optional[UserModel]:
        """Mettre à jour un utilisateur"""
        try:
            update_data = data.model_dump(exclude_unset=True)
            if "password" in update_data:
                update_data["hashed_password"] = self.hash_password(update_data.pop("password"))
            if "email" in update_data:
                existing_user = await self.get_by_email(update_data["email"])
                if existing_user and existing_user.id != id:
                    raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")
            if not update_data:
                raise ValueError("Aucune donnée à mettre à jour")
            result = await self.repository.update(id, update_data)
            return UserModel(**result) if result else None
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de l'utilisateur: {e}")
            raise

    async def delete(self, id: str) -> bool:
        """Supprimer un utilisateur"""
        try:
            return await self.repository.delete(id)
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'utilisateur: {e}")
            raise