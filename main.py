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
from app.controllers.badges_controller import router as badge_router
from app.controllers.actuator_controller import router as actuator_router

import logging
import uvicorn
from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Connexion à MongoDB établie")
    await Database.connect_to_database()
    yield
    logger.info("Connexion à MongoDB fermée")
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
app.include_router(badge_router, prefix="/api/v1")
app.include_router(actuator_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Point d'entrée principal de l'API"""
    return {
        "message": "Bienvenue sur l'API SmartGreenhouse",
        "documentation": "/docs",
        "version": settings.APP_VERSION
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'application"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "environment": settings.ENV
    }

# Point d'entrée pour l'exécution directe
if __name__ == "__main__":
    port = settings.PORT
    reload_option = settings.ENV == "development"
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=reload_option)