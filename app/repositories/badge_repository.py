from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.models.badge_model import BadgeModel
import logging

logger = logging.getLogger(__name__)

class BadgeRepository(BaseRepository[BadgeModel]):
    """Repository pour gérer les badges dans MongoDB"""

    def __init__(self):
        super().__init__("badges")

    async def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer les badges d'un utilisateur"""
        try:
            return await self.get_all(
                filter_query={"user_id": user_id},
                skip=skip,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des badges par user_id: {str(e)}")
            raise
        
    async def get_by_greenhouse_id(self, user_id: str, greenhouse_id: str) -> List[Dict[str, Any]]:
        """Récupérer les badges d'une serre d'un utilisateur"""
        try:
            return await self.get_all(
                filter_query={"user_id": user_id, "greenhouse_id": greenhouse_id})
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des badges par greenhouse_id: {str(e)}")
            raise