from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.models.settings_model import SettingsModel
import logging

logger = logging.getLogger(__name__)

class SettingsRepository(BaseRepository[SettingsModel]):
    """Repository pour gérer les paramètres dans MongoDB"""

    def __init__(self):
        super().__init__("settings")

    async def get_by_user_id(self, user_id: dict) -> Optional[Dict[str, Any]]:
        """Récupérer les paramètres d'un utilisateur"""
        try:
            doc = await self.collection.find_one(user_id)
            if doc:
                doc["id"] = str(doc.pop("_id"))
            return doc
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des paramètres par user_id: {str(e)}")
            raise

    async def count_by_notify(self) -> Dict[str, int]:
        """Compter les paramètres par préférence de notification"""
        try:
            pipeline = [
                {"$group": {"_id": "$notify_by_email", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "notify_by_email": "$_id", "count": 1}}
            ]
            result = await self.collection.aggregate(pipeline).to_list(None)
            counts = {"email_enabled": 0, "email_disabled": 0}
            for item in result:
                if item["notify_by_email"]:
                    counts["email_enabled"] = item["count"]
                else:
                    counts["email_disabled"] = item["count"]
            return counts
        except Exception as e:
            logger.error(f"Erreur lors du comptage des paramètres: {str(e)}")
            raise

    async def search_by_user_id(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Rechercher des paramètres par user_id (recherche partielle)"""
        try:
            return await self.get_all(
                filter_query={"user_id": {"$regex": user_id, "$options": "i"}},
                skip=skip,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des paramètres par user_id: {str(e)}")
            raise
        
    async def get_default(self) -> Optional[dict]:
        """Récupère les paramètres par defaut"""
        try:
            document = await self.collection.find_one({"is_default": True})
            if document:
                document["id"] = str(document.pop("_id"))
                return document
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des paramètres par défaut dans le répostory : {str(e)}")
            raise
    
    async def get_by_greenhouse_id(self, greenhouse_id: dict) -> Optional[Dict]:
        try:
            document = await self.collection.find_one(greenhouse_id)
            if document:
                document["id"] = str(document.pop("_id"))
                return document
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération par greenhouse_id: {str(e)}")
            raise