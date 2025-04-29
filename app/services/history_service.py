from typing import Optional, List, Dict
from app.services.base_service import BaseService
from app.models.history_model import HistoryModel
from app.repositories.history_repository import HistoryRepository
from app.services.greenhouse_service import GreenhouseService
from app.schemas.history_schema import HistoryCreate
from fastapi import HTTPException
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class HistoryService(BaseService[HistoryModel, HistoryCreate, None]):
    """Service pour gérer les opérations liées aux historiques des capteurs"""

    def __init__(self):
        super().__init__()
        self.repository = HistoryRepository()
        self.greenhouse_service = GreenhouseService()

    async def create(self, data: HistoryCreate) -> HistoryModel:
        """Créer une nouvelle entrée historique"""
        try:
            # Vérifier que la serre existe
            greenhouse = await self.greenhouse_service.get_by_id(data.greenhouse_id)
            if not greenhouse:
                raise HTTPException(status_code=400, detail="Serre non trouvée")
            result = await self.repository.create(data.model_dump())
            return HistoryModel(**result)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'historique: {e}")
            raise

    async def get_by_id(self, id: str) -> Optional[HistoryModel]:
        """Récupérer une entrée historique par son ID"""
        try:
            entity = await self.repository.get_by_id(id)
            return HistoryModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'historique: {e}")
            raise

    async def get_by_greenhouse_id(self, greenhouse_id: str, skip: int = 0, limit: int = 100) -> List[HistoryModel]:
        """Récupérer l'historique d'une serre"""
        try:
            entities = await self.repository.get_by_greenhouse_id(greenhouse_id, skip, limit)
            return [HistoryModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'historique par greenhouse_id: {e}")
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[HistoryModel]:
        """Récupérer toutes les entrées historiques"""
        try:
            entities = await self.repository.get_all(skip=skip, limit=limit)
            return [HistoryModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des historiques: {e}")
            raise

    async def count_by_greenhouse_id(self, greenhouse_id: str) -> int:
        """Compter les entrées historiques pour une serre"""
        try:
            return await self.repository.count_by_greenhouse_id(greenhouse_id)
        except Exception as e:
            logger.error(f"Erreur lors du comptage des historiques: {e}")
            raise

    async def search(
        self,
        greenhouse_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        temperature_min: Optional[float] = None,
        temperature_max: Optional[float] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[HistoryModel]:
        """Rechercher des historiques par plage de dates ou valeurs de capteurs"""
        try:
            entities = await self.repository.search(
                greenhouse_id, start_date, end_date, temperature_min, temperature_max, skip, limit
            )
            return [HistoryModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des historiques: {e}")
            raise

    async def update(self, id: str, data: None) -> Optional[HistoryModel]:
        """Mettre à jour une entrée historique (non implémenté)"""
        raise NotImplementedError("Les historiques ne peuvent pas être mis à jour")

    async def delete(self, id: str) -> bool:
        """Supprimer une entrée historique"""
        try:
            return await self.repository.delete(id)
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'historique: {e}")
            raise