from typing import Optional, List, Dict, Any
from app.repositories.base_repository import BaseRepository
from app.models.user_model import UserModel
import logging

logger = logging.getLogger(__name__)

class UserRepository(BaseRepository[UserModel]):
    """Repository pour gérer les utilisateurs dans MongoDB"""

    def __init__(self):
        super().__init__("users")

    async def get_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Récupérer un utilisateur par son email"""
        try:
            doc = await self.collection.find_one({"email": email})
            if doc:
                doc["id"] = str(doc.pop("_id"))
            return doc
        except Exception as e:
            logger.error(f"Erreur lors de la récupération par email: {str(e)}")
            raise

    async def count_by_role(self) -> Dict[str, int]:
        """Compter les utilisateurs par rôle (admin/non-admin)"""
        try:
            pipeline = [
                {"$group": {"_id": "$is_admin", "count": {"$sum": 1}}},
                {"$project": {"_id": 0, "is_admin": "$_id", "count": 1}}
            ]
            result = await self.collection.aggregate(pipeline).to_list(None)
            counts = {"admin": 0, "non_admin": 0}
            for item in result:
                if item["is_admin"]:
                    counts["admin"] = item["count"]
                else:
                    counts["non_admin"] = item["count"]
            return counts
        except Exception as e:
            logger.error(f"Erreur lors du comptage des utilisateurs: {str(e)}")
            raise

    async def search_by_email(self, email: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Rechercher des utilisateurs par email (recherche partielle)"""
        try:
            return await self.get_all(
                filter_query={"email": {"$regex": email, "$options": "i"}},
                skip=skip,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Erreur lors de la recherche des utilisateurs par email: {str(e)}")
            raise