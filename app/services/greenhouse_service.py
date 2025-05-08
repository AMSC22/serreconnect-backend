from typing import Optional, List
from app.services.base_service import BaseService
from app.models.greenhouse_model import GreenhouseModel
from app.repositories.greenhouse_repository import GreenhouseRepository
from app.services.user_service import UserService
from app.schemas.greenhouse_schema import GreenhouseCreate, GreenhouseUpdate
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class GreenhouseService(BaseService[GreenhouseModel, GreenhouseCreate, GreenhouseUpdate]):
    """Service pour gérer les opérations liées aux serres"""

    def __init__(self):
        super().__init__()
        self.repository = GreenhouseRepository()
        self.user_service = UserService()

    async def create(self, data: GreenhouseCreate) -> GreenhouseModel:
        """Créer une nouvelle serre"""
        try:
            # Vérifier que l'utilisateur existe
            user = await self.user_service.get_by_id(data.user_id)
            if not user:
                raise HTTPException(status_code=400, detail="Utilisateur non trouvé")
            result = await self.repository.create(data.model_dump())
            return GreenhouseModel(**result)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur lors de la création de la serre: {e}")
            raise

    async def get_by_id(self, id: str) -> Optional[GreenhouseModel]:
        """Récupérer une serre par son ID"""
        try:
            entity = await self.repository.get_by_id(id)
            return GreenhouseModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la serre: {e}")
            raise

    async def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[GreenhouseModel]:
        """Récupérer les serres d'un utilisateur"""
        try:
            entities = await self.repository.get_by_user_id(user_id, skip, limit)
            return [GreenhouseModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des serres par user_id: {e}")
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[GreenhouseModel]:
        """Récupérer toutes les serres"""
        try:
            entities = await self.repository.get_all(skip=skip, limit=limit)
            return [GreenhouseModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des serres: {e}")
            raise

    async def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[GreenhouseModel]:
        """Rechercher des serres par nom"""
        try:
            entities = await self.repository.search_by_name(name, skip, limit)
            return [GreenhouseModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des serres: {e}")
            raise

    async def update(self, id: str, data: GreenhouseUpdate) -> Optional[GreenhouseModel]:
        """Mettre à jour une serre"""
        try:
            update_data = data.model_dump(exclude_unset=True)
            if not update_data:
                raise ValueError("Aucune donnée à mettre à jour")
            result = await self.repository.update(id, update_data)
            return GreenhouseModel(**result) if result else None
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la serre: {e}")
            raise

    async def delete(self, id: str) -> bool:
        """Supprimer une serre"""
        try:
            return await self.repository.delete(id)
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de la serre: {e}")
            raise
        
    async def get_camera_url(self, greenhouse_id: str) -> str:
        # TODO: Implémenter la logique (par exemple, récupérer l'URL depuis une caméra IP)
        return f"rtsp://camera-{greenhouse_id}:554/stream"