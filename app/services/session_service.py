from typing import Optional, List
from app.services.base_service import BaseService
from app.models.session_model import SessionModel
from app.repositories.session_repository import SessionRepository
from app.schemas.session_schema import SessionCreate, SessionUpdate, SessionResponse
from fastapi import HTTPException
import uuid
import logging

logger = logging.getLogger(__name__)

class SessionService(BaseService[SessionModel, SessionCreate, SessionUpdate]):
    """Service pour gérer les sessions utilisateur"""

    def __init__(self):
        super().__init__()
        self.repository = SessionRepository()

    async def create(self, data: SessionCreate) -> SessionModel:
        """Créer une nouvelle session"""
        try:
            session_id = str(uuid.uuid4())
            session_data = data.model_dump()
            session_data["session_id"] = session_id
            result = await self.repository.create(session_data)
            return SessionModel(**result)
        except Exception as e:
            logger.error(f"Erreur lors de la création de la session: {e}")
            raise

    async def get_by_id(self, id: str) -> Optional[SessionModel]:
        """Récupérer une session par son ID"""
        try:
            entity = await self.repository.get_by_id(id)
            return SessionModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la session: {e}")
            raise

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[SessionModel]:
        """Récupérer toutes les sessions"""
        try:
            entities = await self.repository.get_all(skip=skip, limit=limit)
            return [SessionModel(**entity) for entity in entities]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des sessions: {e}")
            raise

    async def update(self, id: str, data: SessionUpdate) -> Optional[SessionModel]:
        """Mettre à jour une session"""
        try:
            update_data = data.model_dump(exclude_unset=True)
            if not update_data:
                return await self.get_by_id(id)
            result = await self.repository.update(id, update_data)
            return SessionModel(**result) if result else None
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la session: {e}")
            raise

    async def delete(self, id: str) -> bool:
        """Supprimer une session"""
        try:
            return await self.repository.delete(id)
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de la session: {e}")
            raise

    async def get_by_session_id(self, session_id: str) -> Optional[SessionModel]:
        """Récupérer une session par son session_id"""
        try:
            entity = await self.repository.get_by_session_id(session_id)
            return SessionModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de la session: {e}")
            raise

    async def update_last_activity(self, session_id: str) -> Optional[SessionModel]:
        """Mettre à jour la dernière activité"""
        try:
            entity = await self.repository.update_last_activity(session_id)
            return SessionModel(**entity) if entity else None
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de la session: {e}")
            raise

    async def invalidate_session(self, session_id: str) -> bool:
        """Invalider une session"""
        try:
            return await self.repository.invalidate_session(session_id)
        except Exception as e:
            logger.error(f"Erreur lors de l'invalidation de la session: {e}")
            raise