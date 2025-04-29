from typing import Optional, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.models.session_model import SessionModel
from app.utils.time_utils import get_local_time
import logging

logger = logging.getLogger(__name__)

class SessionRepository(BaseRepository[SessionModel]):
    """Repository pour gérer les sessions dans MongoDB"""

    def __init__(self):
        super().__init__("sessions")

    async def get_by_session_id(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Récupérer une session par son session_id"""
        try:
            doc = await self.collection.find_one({"session_id": session_id, "is_active": True})
            if doc:
                doc["id"] = str(doc.pop("_id"))
            return doc
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la session: {str(e)}")
            raise

    async def update_last_activity(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Mettre à jour la dernière activité d'une session"""
        try:
            result = await self.collection.find_one_and_update(
                {"session_id": session_id, "is_active": True},
                {"$set": {"last_activity": get_local_time()}},
                return_document=True
            )
            if result:
                result["id"] = str(result.pop("_id"))
            return result
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la session: {str(e)}")
            raise

    async def invalidate_session(self, session_id: str) -> bool:
        """Invalider une session"""
        try:
            result = await self.collection.update_one(
                {"session_id": session_id},
                {"$set": {"is_active": False}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Erreur lors de l'invalidation de la session: {str(e)}")
            raise