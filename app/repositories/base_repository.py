from typing import Optional, List, Dict, Any, Generic, TypeVar
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from app.config.database import Database
import logging
from datetime import datetime
from app.utils.time_utils import get_local_time

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Repository de base avec des méthodes CRUD génériques"""
    def __init__(self, collection_name: str):
        self.collection: AsyncIOMotorCollection = Database.smart_greenhouse_db[collection_name]
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Créer un document"""
        try:
            data["created_at"] = get_local_time()
            data["updated_at"] = get_local_time()
            result = await self.collection.insert_one(data)
            created_doc = await self.get_by_id(str(result.inserted_id))
            self.logger.info(f"Document créé dans {self.collection.name}: {str(result.inserted_id)}")
            return created_doc
        except Exception as e:
            self.logger.error(f"Erreur lors de la création: {str(e)}")
            raise

    async def get_by_id(self, id: str) -> Optional[Dict[str, Any]]:
        """Récupérer un document par son ID"""
        try:
            doc = await self.collection.find_one({"_id": ObjectId(id)})
            if doc:
                doc["id"] = str(doc.pop("_id"))
            return doc
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération par ID: {str(e)}")
            raise

    async def get_all(
        self,
        filter_query: Dict[str, Any] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Récupérer tous les documents avec pagination"""
        try:
            filter_query = filter_query or {}
            cursor = self.collection.find(filter_query).skip(skip).limit(limit)
            docs = []
            async for doc in cursor:
                doc["id"] = str(doc.pop("_id"))
                docs.append(doc)
            return docs
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération: {str(e)}")
            raise

    async def update(self, id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Mettre à jour un document"""
        try:
            data["updated_at"] = get_local_time()
            result = await self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": data}
            )
            if result.modified_count:
                updated_doc = await self.get_by_id(id)
                self.logger.info(f"Document mis à jour: {id}")
                return updated_doc
            return None
        except Exception as e:
            self.logger.error(f"Erreur lors de la mise à jour: {str(e)}")
            raise

    async def delete(self, id: str) -> bool:
        """Supprimer un document"""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(id)})
            if result.deleted_count > 0:
                self.logger.info(f"Document supprimé: {id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Erreur lors de la suppression: {str(e)}")
            raise