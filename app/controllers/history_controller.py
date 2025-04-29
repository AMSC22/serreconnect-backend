from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from app.services.history_service import HistoryService
from app.services.greenhouse_service import GreenhouseService
from app.schemas.history_schema import HistoryCreate, HistoryResponse
from app.auth.jwt_handler import get_current_user
from datetime import datetime

router = APIRouter(
    prefix="/history",
    tags=["history"]
)

@router.post("/", response_model=HistoryResponse)
async def create_history(history: HistoryCreate, current_user: dict = Depends(get_current_user)):
    """Créer une nouvelle entrée historique"""
    try:
        greenhouse = await GreenhouseService().get_by_id(history.greenhouse_id)
        if not greenhouse:
            raise HTTPException(status_code=404, detail="Serre non trouvée")
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette serre")
        service = HistoryService()
        result = await service.create(history)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/count/{greenhouse_id}", response_model=int)
async def count_history(greenhouse_id: str, current_user: dict = Depends(get_current_user)):
    """Compter les entrées historiques pour une serre"""
    try:
        greenhouse = await GreenhouseService().get_by_id(greenhouse_id)
        if not greenhouse:
            raise HTTPException(status_code=404, detail="Serre non trouvée")
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette serre")
        service = HistoryService()
        return await service.count_by_greenhouse_id(greenhouse_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=List[HistoryResponse])
async def search_history(
    greenhouse_id: str = Query(..., description="ID de la serre"),
    start_date: Optional[datetime] = Query(None, description="Date de début (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Date de fin (ISO format)"),
    temperature_min: Optional[float] = Query(None, description="Température minimum (°C)"),
    temperature_max: Optional[float] = Query(None, description="Température maximum (°C)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Rechercher des historiques par plage de dates ou valeurs de capteurs"""
    try:
        greenhouse = await GreenhouseService().get_by_id(greenhouse_id)
        if not greenhouse:
            raise HTTPException(status_code=404, detail="Serre non trouvée")
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette serre")
        service = HistoryService()
        return await service.search(greenhouse_id, start_date, end_date, temperature_min, temperature_max, skip, limit)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=HistoryResponse)
async def get_history(id: str, current_user: dict = Depends(get_current_user)):
    """Récupérer une entrée historique par son ID"""
    try:
        service = HistoryService()
        result = await service.get_by_id(id)
        if not result:
            raise HTTPException(status_code=404, detail="Entrée historique non trouvée")
        greenhouse = await GreenhouseService().get_by_id(result.greenhouse_id)
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette entrée historique")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/greenhouse/{greenhouse_id}", response_model=List[HistoryResponse])
async def get_history_by_greenhouse(
    greenhouse_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Récupérer l'historique d'une serre"""
    try:
        greenhouse = await GreenhouseService().get_by_id(greenhouse_id)
        if not greenhouse:
            raise HTTPException(status_code=404, detail="Serre non trouvée")
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette serre")
        service = HistoryService()
        return await service.get_by_greenhouse_id(greenhouse_id, skip, limit)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[HistoryResponse])
async def get_all_history(current_user: dict = Depends(get_current_user)):
    """Récupérer toutes les entrées historiques (admins uniquement)"""
    try:
        if not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
        service = HistoryService()
        return await service.get_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
async def delete_history(id: str, current_user: dict = Depends(get_current_user)):
    """Supprimer une entrée historique"""
    try:
        service = HistoryService()
        history = await service.get_by_id(id)
        if not history:
            raise HTTPException(status_code=404, detail="Entrée historique non trouvée")
        greenhouse = await GreenhouseService().get_by_id(history.greenhouse_id)
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette entrée historique")
        result = await service.delete(id)
        if not result:
            raise HTTPException(status_code=404, detail="Entrée historique non trouvée")
        return {"message": "Entrée historique supprimée avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))