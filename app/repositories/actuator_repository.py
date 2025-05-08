from typing import List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.models.actuator_model import ActuatorModel
import logging
from bson import ObjectId

logger = logging.getLogger(__name__)

class ActuatorRepository(BaseRepository[ActuatorModel]):
    """Repository pour gérer les actionneurs dans MongoDB"""

    def __init__(self):
        super().__init__("actuators")

    async def get_by_greenhouse_id(self, greenhouse_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Récupérer les actionneurs d'une serre"""
        try:
            return await self.get_all(filter_query={"greenhouse_id": greenhouse_id}, skip=skip, limit=limit)
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des actionneurs par greenhouse_id: {str(e)}")
            raise
    
    async def delete(self, id: str) -> bool:
        try:
            result = await self.collection.delete_one({"_id": ObjectId(id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'actionneur: {str(e)}")
            raise