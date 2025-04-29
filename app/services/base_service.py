from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel
import logging

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

logger = logging.getLogger(__name__)

class BaseService(ABC, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Service de base avec des méthodes CRUD génériques"""
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    async def create(self, data: CreateSchemaType) -> ModelType:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[ModelType]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        pass

    @abstractmethod
    async def update(self, id: str, data: UpdateSchemaType) -> Optional[ModelType]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass