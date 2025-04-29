from typing import List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.models.alert_model import AlertModel
import logging

logger = logging.getLogger(__name__)

class AlertRepository(BaseRepository[AlertModel]):
    """Repository pour gérer les alertes dans MongoDB"""

    def __init__(self):
        super().__init__("alerts")

    async def get_by_greenhouse_id(self, greenhouse_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer les alertes d'une serre"""
        try:
            return await self.get_all(filter_query={"greenhouse_id": greenhouse_id}, skip=skip, limit=limit)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des alertes par greenhouse_id: {str(e)}")
            raise

    async def count_by_status(self) -> Dict[str, int]:
        """Compter les alertes par statut (résolues/non résolues)"""
        try:
            pipeline = [
                {"$group": {"_id": "$is_resolved", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "is_resolved": "$_id", "count": 1}}
            ]
            result = await self.collection.aggregate(pipeline).to_list(None)
            counts = {"resolved": 0, "unresolved": 0}
            for item in result:
                if item["is_resolved"]:
                    counts["resolved"] = item["count"]
                else:
                    counts["unresolved"] = item["count"]
            return counts
        except Exception as e:
            logger.error(f"Erreur lors du comptage des alertes: {str(e)}")
            raise

    async def search(self, query: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Rechercher des alertes par type ou message"""
        try:
            return await self.get_all(
                filter_query={
                    "$or": [
                        {"type": {"$regex": query, "$options": "i"}},
                        {"message": {"$regex": query, "$options": "i"}}
                    ]
                },
                skip=skip,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des alertes: {str(e)}")
            raise