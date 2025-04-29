from typing import Optional, List, Dict
from app.services.base_service import BaseService
from app.models.alert_model import AlertModel
from app.repositories.alert_repository import AlertRepository
from app.services.greenhouse_service import GreenhouseService
from app.schemas.alert_schema import AlertCreate, AlertUpdate
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class AlertService(BaseService[AlertModel, AlertCreate, AlertUpdate]):
    """Service pour gérer les opérations liées aux alertes"""

    def __init__(self):
        super().__init__()
        self.repository = AlertRepository()
        self.greenhouse_service = GreenhouseService()

    async def create(self, data: AlertCreate) -> AlertModel:
        """Créer une nouvelle alerte"""
        try:
            # Vérifier que la serre existe
            greenhouse = await self.greenhouse_service.get_by_id(data.greenhouse_id)
            if not greenhouse:
                raise HTTPException(status_code=400, detail="Serre non trouvée")
            result = await self.repository.create(data.model_dump())
            return AlertModel(**result)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'alerte: {e}")
            raise

    async def get_by_id(self, id: str) -> Optional[AlertModel]:
        """Récupérer une alerte par son ID"""
        try:
            entity = await self.repository.get_by_id(id)
            return AlertModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'alerte: {e}")
            raise

    async def get_by_greenhouse_id(self, greenhouse_id: str, skip: int = 0, limit: int = 100) -> List[AlertModel]:
        """Récupérer les alertes d'une serre"""
        try:
            entities = await self.repository.get_by_greenhouse_id(greenhouse_id, skip, limit)
            return [AlertModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des alertes par greenhouse_id: {e}")
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[AlertModel]:
        """Récupérer toutes les alertes"""
        try:
            entities = await self.repository.get_all(skip=skip, limit=limit)
            return [AlertModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des alertes: {e}")
            raise

    async def count_by_status(self) -> Dict[str, int]:
        """Compter les alertes par statut"""
        try:
            return await self.repository.count_by_status()
        except Exception as e:
            logger.error(f"Erreur lors du comptage des alertes: {e}")
            raise

    async def search(self, query: str, skip: int = 0, limit: int = 100) -> List[AlertModel]:
        """Rechercher des alertes par type ou message"""
        try:
            entities = await self.repository.search(query, skip, limit)
            return [AlertModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des alertes: {e}")
            raise

    async def update(self, id: str, data: AlertUpdate) -> Optional[AlertModel]:
        """Mettre à jour une alerte"""
        try:
            update_data = data.model_dump(exclude_unset=True)
            if not update_data:
                raise ValueError("Aucune donnée à mettre à jour")
            result = await self.repository.update(id, update_data)
            return AlertModel(**result) if result else None
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de l'alerte: {e}")
            raise

    async def delete(self, id: str) -> bool:
        """Supprimer une alerte"""
        try:
            return await self.repository.delete(id)
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'alerte: {e}")
            raise