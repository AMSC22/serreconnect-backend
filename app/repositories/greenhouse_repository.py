from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.models.greenhouse_model import GreenhouseModel
import logging

logger = logging.getLogger(__name__)

class GreenhouseRepository(BaseRepository[GreenhouseModel]):
    """Repository pour gérer les serres dans MongoDB"""

    def __init__(self):
        super().__init__("greenhouses")

    async def get_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer les serres d'un utilisateur"""
        try:
            return await self.get_all(filter_query={"user_id": user_id}, skip=skip, limit=limit)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des serres par user_id: {str(e)}")
            raise

    async def search_by_name(self, name: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Rechercher des serres par nom (recherche partielle)"""
        try:
            return await self.get_all(
                filter_query={"name": {"$regex": name, "$options": "i"}},  # Recherche insensible à la casse
                skip=skip,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des serres par nom: {str(e)}")
            raise