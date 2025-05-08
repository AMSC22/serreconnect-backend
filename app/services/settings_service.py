from typing import Optional, List, Dict
from app.services.base_service import BaseService
from app.models.settings_model import SettingsModel
from app.repositories.settings_repository import SettingsRepository
from app.services.user_service import UserService
from app.schemas.settings_schema import SettingsCreate, SettingsUpdate
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class SettingsService(BaseService[SettingsModel, SettingsCreate, SettingsUpdate]):
    """Service pour gérer les opérations liées aux paramètres"""

    def __init__(self):
        super().__init__()
        self.repository = SettingsRepository()
        self.user_service = UserService()

    async def create(self, data: SettingsCreate) -> SettingsModel:
        """Créer de nouveaux paramètres"""
        try:
            # Vérifier que l'utilisateur existe
            user = await self.user_service.get_by_id(data.user_id)
            if not user:
                raise HTTPException(status_code=400, detail="Utilisateur non trouvé")
            # Vérifier si des paramètres existent déjà
            existing_settings = await self.get_by_user_id(data.user_id)
            if existing_settings:
                raise HTTPException(status_code=400, detail="Des paramètres existent déjà pour cet utilisateur")
            result = await self.repository.create(data.model_dump())
            return SettingsModel(**result)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur lors de la création des paramètres: {e}")
            raise

    async def get_by_id(self, id: str) -> Optional[SettingsModel]:
        """Récupérer des paramètres par leur ID"""
        try:
            entity = await self.repository.get_by_id(id)
            return SettingsModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des paramètres: {e}")
            raise

    async def get_by_user_id(self, user_id: dict) -> Optional[SettingsModel]:
        """Récupérer les paramètres d'un utilisateur"""
        try:
            entity = await self.repository.get_by_user_id(user_id)
            return SettingsModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des paramètres par user_id: {e}")
            raise
    
    async def get_by_greenhouse_id(self, greenhouse_id: dict) -> Optional[SettingsModel]:
        """Récupérer les paramètres d'une Serre"""
        try:
            entity = await self.repository.get_by_greenhouse_id(greenhouse_id)
            return SettingsModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des paramètres par greenhouse_id: {e}")
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[SettingsModel]:
        """Récupérer tous les paramètres"""
        try:
            entities = await self.repository.get_all(skip=skip, limit=limit)
            return [SettingsModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des paramètres: {e}")
            raise

    async def count_by_notify(self) -> Dict[str, int]:
        """Compter les paramètres par préférence de notification"""
        try:
            return await self.repository.count_by_notify()
        except Exception as e:
            logger.error(f"Erreur lors du comptage des paramètres: {e}")
            raise

    async def search_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[SettingsModel]:
        """Rechercher des paramètres par user_id"""
        try:
            entities = await self.repository.search_by_user_id(user_id, skip, limit)
            return [SettingsModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des paramètres: {e}")
            raise

    async def update(self, id: str, data: SettingsUpdate) -> Optional[SettingsModel]:
        """Mettre à jour des paramètres"""
        try:
            update_data = data.model_dump(exclude_unset=True)
            if not update_data:
                raise ValueError("Aucune donnée à mettre à jour")
            result = await self.repository.update(id, update_data)
            return SettingsModel(**result) if result else None
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour des paramètres: {e}")
            raise

    async def delete(self, id: str) -> bool:
        """Supprimer des paramètres"""
        try:
            return await self.repository.delete(id)
        except Exception as e:
            logger.error(f"Erreur lors de la suppression des paramètres: {e}")
            raise
        
    async def get_default_settings(self) -> Optional[dict]:
        """Récupérer les valeurs par défaut des paramètres"""
        try:
            entity = await self.repository.get_default()
            return entity if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des paramètres par défaut dans le service : {str(e)}")
            raise