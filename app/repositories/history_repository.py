from typing import List, Dict, Any, Optional
from app.repositories.base_repository import BaseRepository
from app.models.history_model import HistoryModel
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class HistoryRepository(BaseRepository[HistoryModel]):
    """Repository pour gérer les historiques des capteurs dans MongoDB"""

    def __init__(self):
        super().__init__("history")

    async def get_by_greenhouse_id(self, greenhouse_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer l'historique d'une serre"""
        try:
            return await self.get_all(
                filter_query={"greenhouse_id": greenhouse_id},
                skip=skip,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'historique par greenhouse_id: {str(e)}")
            raise

    async def count_by_greenhouse_id(self, greenhouse_id: str) -> int:
        """Compter les entrées historiques pour une serre"""
        try:
            return await self.collection.count_documents({"greenhouse_id": greenhouse_id})
        except Exception as e:
            logger.error(f"Erreur lors du comptage des historiques: {str(e)}")
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
    ) -> List[Dict[str, Any]]:
        """Rechercher des historiques par plage de dates ou valeurs de capteurs"""
        try:
            filter_query = {"greenhouse_id": greenhouse_id}
            if start_date or end_date:
                filter_query["recorded_at"] = {}
                if start_date:
                    filter_query["recorded_at"]["$gte"] = start_date
                if end_date:
                    filter_query["recorded_at"]["$lte"] = end_date
            if temperature_min is not None:
                filter_query["temperature"] = filter_query.get("temperature", {})
                filter_query["temperature"]["$gte"] = temperature_min
            if temperature_max is not None:
                filter_query["temperature"] = filter_query.get("temperature", {})
                filter_query["temperature"]["$lte"] = temperature_max
            return await self.get_all(filter_query=filter_query, skip=skip, limit=limit)
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des historiques: {str(e)}")
            raise