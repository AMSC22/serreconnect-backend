from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None
    smart_greenhouse_db = None

    @classmethod
    async def connect_to_database(cls):
        try:
            logger.info("Connexion à MongoDB...")
            cls.client = AsyncIOMotorClient(
                settings.MONGODB_URL,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                retryWrites=True,
                w="majority"
            )
            cls.smart_greenhouse_db = cls.client[settings.MONGODB_DB_NAME]
            await cls.smart_greenhouse_db.command("ping")
            # Créer des index
            await cls.smart_greenhouse_db["users"].create_index("email", unique=True)
            await cls.smart_greenhouse_db["greenhouses"].create_index("user_id")
            await cls.smart_greenhouse_db["alerts"].create_index("greenhouse_id")
            await cls.smart_greenhouse_db["history"].create_index("greenhouse_id")
            await cls.smart_greenhouse_db["history"].create_index("recorded_at")
            await cls.smart_greenhouse_db["settings"].create_index("user_id", unique=True)
            await cls.smart_greenhouse_db["sessions"].create_index("session_id", unique=True)
            logger.info("Connecté à la base de données SmartGreenhouse")
        except Exception as e:
            logger.error(f"Erreur de connexion à MongoDB: {str(e)}")
            raise

    @classmethod
    async def close_database_connection(cls):
        logger.info("Fermeture de la connexion à MongoDB...")
        if cls.client:
            cls.client.close()
            logger.info("Connexion fermée")