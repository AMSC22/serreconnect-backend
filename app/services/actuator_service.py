from typing import List, Optional
from app.models.actuator_model import ActuatorModel
from app.repositories.actuator_repository import ActuatorRepository
from app.schemas.actuator_schema import ActuatorCreate, ActuatorUpdate, ActuatorResponse
from app.services.base_service import BaseService
import logging

logger = logging.getLogger(__name__)

class ActuatorService(BaseService[ActuatorModel, ActuatorCreate, ActuatorUpdate]):
    def __init__(self):
        self.repository = ActuatorRepository()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ActuatorResponse]:
        """Récupérer tous les actionneurs"""
        try:
            actuators = await self.repository.get_all(skip, limit)
            return [ActuatorResponse(**actuator) for actuator in actuators]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de tous les actionneurs: {str(e)}")
            raise
    
    async def get_by_id(self, id: str) -> Optional[ActuatorResponse]:
        """Récupérer un actionneur par son ID"""
        try:
            actuator = await self.repository.get_by_id(id)
            if actuator:
                return ActuatorResponse(**actuator)
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la récupération de l'actionneur par ID: {str(e)}")
            raise

    async def create(self, actuator: ActuatorCreate) -> ActuatorResponse:
        """Créer un nouvel actionneur"""
        try:
            actuator_dict = actuator.dict()
            created = await self.repository.create(actuator_dict)
            return ActuatorResponse(**created)
        except Exception as e:
            logger.error(f"Erreur lors de la création de l'actionneur: {str(e)}")
            raise
    
    async def get_by_greenhouse_id(self, greenhouse_id: str, skip: int = 0, limit: int = 100) -> List[ActuatorResponse]:
        """Récupérer les actionneurs d'une serre"""
        try:
            actuators = await self.repository.get_by_greenhouse_id(greenhouse_id, skip, limit)
            return [ActuatorResponse(**actuator) for actuator in actuators]
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des actionneurs: {str(e)}")
            raise
    
    async def update(self, id: str, actuator_update: ActuatorUpdate) -> Optional[ActuatorResponse]:
        """Mettre à jour un actionneur"""
        try:
            update_dict = actuator_update.dict(exclude_unset=True)
            updated = await self.repository.update(id, update_dict)
            if updated:
                return ActuatorResponse(**updated)
            return None
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour de l'actionneur: {str(e)}")
            raise
            
    async def delete(self, id: str) -> bool:
        try:
            return await self.repository.delete(id)
        except Exception as e:
            logger.error(f"Erreur lors de la suppression de l'actionneur: {str(e)}")
            raise