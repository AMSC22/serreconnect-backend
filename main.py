from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.config.database import Database
from app.controllers.user_controller import router as user_router
from app.controllers.greenhouse_controller import router as greenhouse_router
from app.controllers.alert_controller import router as alert_router
from app.controllers.history_controller import router as history_router
from app.controllers.settings_controller import router as settings_router
from app.controllers.auth_controller import router as auth_router
import logging
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Démarrage de l'application...")
    await Database.connect_to_database()
    yield
    logger.info("Arrêt de l'application...")
    await Database.close_database_connection()

app = FastAPI(
    title="SmartGreenhouse API",
    description="API pour la gestion des serres intelligentes.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")
app.include_router(greenhouse_router, prefix="/api/v1")
app.include_router(alert_router, prefix="/api/v1")
app.include_router(history_router, prefix="/api/v1")
app.include_router(settings_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'application"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENV
    }