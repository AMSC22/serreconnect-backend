from typing import Optional, List
from app.services.base_service import BaseService
from app.models.badge_model import BadgeModel
from app.repositories.badge_repository import BadgeRepository
from app.schemas.badge_schema import BadgeCreate, BadgeUpdate
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class BadgeService(BaseService[BadgeModel, BadgeCreate, BadgeUpdate]):
    """Service pour gérer les opérations liées aux badges"""

    def __init__(self):
        super().__init__()
        self.repository = BadgeRepository()

    async def create(self, data: BadgeCreate, current_user_id: str) -> BadgeModel:
        """Créer un nouveau badge"""
        try:
            badge_data = data.model_dump()
            badge_data["user_id"] = current_user_id
            result = await self.repository.create(badge_data)
            return BadgeModel(**result)
        except Exception as e:
            logger.error(f"Erreur lors de la création du badge: {e}")
            raise

    async def get_by_id(self, id: str) -> Optional[BadgeModel]:
        """Récupérer un badge par son ID"""
        try:
            entity = await self.repository.get_by_id(id)
            return BadgeModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du badge: {e}")
            raise

    async def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[BadgeModel]:
        """Récupérer les badges d'un utilisateur"""
        try:
            entities = await self.repository.get_by_user_id(user_id, skip, limit)
            return [BadgeModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des badges par user_id: {e}")
            raise
    
    async def get_by_greenhouse_id(self, user_id: str, greenhouse_id: str) -> List[BadgeModel]:
        """Récupérer les badges d'une serre d'un utilisateur"""
        try:
            entities = await self.repository.get_by_greenhouse_id(user_id, greenhouse_id)
            return [BadgeModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des badges par greenhouse_id: {e}")
            raise

    async def update(self, id: str, data: BadgeUpdate, current_user_id: str) -> Optional[BadgeModel]:
        """Mettre à jour un badge"""
        try:
            badge = await self.get_by_id(id)
            if not badge:
                raise HTTPException(status_code=404, detail="Badge non trouvé")
            if badge.user_id != current_user_id:
                raise HTTPException(status_code=403, detail="Non autorisé")
            update_data = data.model_dump(exclude_unset=True)
            if not update_data:
                raise ValueError("Aucune donnée à mettre à jour")
            result = await self.repository.update(id, update_data)
            return BadgeModel(**result) if result else None
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du badge: {e}")
            raise

    async def delete(self, id: str, current_user_id: str) -> bool:
        """Supprimer un badge"""
        try:
            badge = await self.get_by_id(id)
            if not badge:
                raise HTTPException(status_code=404, detail="Badge non trouvé")
            if badge.user_id != current_user_id:
                raise HTTPException(status_code=403, detail="Non autorisé")
            return await self.repository.delete(id)
        except Exception as e:
            logger.error(f"Erreur lors de la suppression du badge: {e}")
            raise
    
    async def get_all(self, id: str) -> List[BadgeModel]:
        """Récupérer tous les badges"""
        try:
            entities = await self.repository.get_all({"user_id": id})
            return [BadgeModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des badges: {e}")
            raise