from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict
from app.services.alert_service import AlertService
from app.services.greenhouse_service import GreenhouseService
from app.schemas.alert_schema import AlertCreate, AlertUpdate, AlertResponse
from app.auth.jwt_handler import get_current_user

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"]
)

@router.post("/", response_model=AlertResponse)
async def create_alert(alert: AlertCreate, current_user: dict = Depends(get_current_user)):
    """Créer une nouvelle alerte"""
    try:
        greenhouse_service = GreenhouseService()
        greenhouse = await greenhouse_service.get_by_id(alert.greenhouse_id)
        if not greenhouse:
            raise HTTPException(status_code=404, detail="Serre non trouvée")
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette serre")
        service = AlertService()
        result = await service.create(alert)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/count", response_model=Dict[str, int])
async def count_alerts(current_user: dict = Depends(get_current_user)):
    """Compter les alertes par statut"""
    try:
        service = AlertService()
        results = await service.count_by_status()
        if not current_user["is_admin"]:
            # Filtrer pour les serres de l'utilisateur
            user_greenhouses = await GreenhouseService().get_by_user_id(current_user["user_id"])
            greenhouse_ids = [g.id for g in user_greenhouses]
            alerts = await service.get_all()
            resolved = sum(1 for a in alerts if a.greenhouse_id in greenhouse_ids and a.is_resolved)
            unresolved = sum(1 for a in alerts if a.greenhouse_id in greenhouse_ids and not a.is_resolved)
            results = {"resolved": resolved, "unresolved": unresolved}
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=List[AlertResponse])
async def search_alerts(
    query: str = Query(..., description="Type ou message à rechercher"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Rechercher des alertes par type ou message"""
    try:
        service = AlertService()
        results = await service.search(query, skip, limit)
        if not current_user["is_admin"]:
            user_greenhouses = await GreenhouseService().get_by_user_id(current_user["user_id"])
            greenhouse_ids = [g.id for g in user_greenhouses]
            results = [r for r in results if r.greenhouse_id in greenhouse_ids]
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=AlertResponse)
async def get_alert(id: str, current_user: dict = Depends(get_current_user)):
    """Récupérer une alerte par son ID"""
    try:
        service = AlertService()
        result = await service.get_by_id(id)
        if not result:
            raise HTTPException(status_code=404, detail="Alerte non trouvée")
        greenhouse = await GreenhouseService().get_by_id(result.greenhouse_id)
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette alerte")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/greenhouse/{greenhouse_id}", response_model=List[AlertResponse])
async def get_alerts_by_greenhouse(greenhouse_id: str, current_user: dict = Depends(get_current_user)):
    """Récupérer les alertes d'une serre"""
    try:
        greenhouse = await GreenhouseService().get_by_id(greenhouse_id)
        if not greenhouse:
            raise HTTPException(status_code=404, detail="Serre non trouvée")
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette serre")
        service = AlertService()
        return await service.get_by_greenhouse_id(greenhouse_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[AlertResponse])
async def get_all_alerts(current_user: dict = Depends(get_current_user)):
    """Récupérer toutes les alertes (admins uniquement)"""
    try:
        if not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
        service = AlertService()
        return await service.get_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}", response_model=AlertResponse)
async def update_alert(id: str, alert_update: AlertUpdate, current_user: dict = Depends(get_current_user)):
    """Mettre à jour une alerte"""
    try:
        service = AlertService()
        alert = await service.get_by_id(id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alerte non trouvée")
        greenhouse = await GreenhouseService().get_by_id(alert.greenhouse_id)
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette alerte")
        result = await service.update(id, alert_update)
        if not result:
            raise HTTPException(status_code=404, detail="Alerte non trouvée")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
async def delete_alert(id: str, current_user: dict = Depends(get_current_user)):
    """Supprimer une alerte"""
    try:
        service = AlertService()
        alert = await service.get_by_id(id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alerte non trouvée")
        greenhouse = await GreenhouseService().get_by_id(alert.greenhouse_id)
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette alerte")
        result = await service.delete(id)
        if not result:
            raise HTTPException(status_code=404, detail="Alerte non trouvée")
        return {"message": "Alerte supprimée avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))