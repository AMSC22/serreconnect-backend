from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict
from app.services.settings_service import SettingsService
from app.schemas.settings_schema import SettingsCreate, SettingsUpdate, SettingsResponse
from app.auth.jwt_handler import get_current_user, get_current_admin

router = APIRouter(
    prefix="/settings",
    tags=["settings"]
)

@router.post("/", response_model=SettingsResponse)
async def create_settings(settings: SettingsCreate, current_user: dict = Depends(get_current_user)):
    """Créer de nouveaux paramètres"""
    try:
        if settings.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Vous ne pouvez créer des paramètres que pour votre propre utilisateur")
        service = SettingsService()
        result = await service.create(settings)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/count", response_model=Dict[str, int], dependencies=[Depends(get_current_admin)])
async def count_settings():
    """Compter les paramètres par préférence de notification (admin uniquement)"""
    try:
        service = SettingsService()
        return await service.count_by_notify()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=List[SettingsResponse], dependencies=[Depends(get_current_admin)])
async def search_settings(
    user_id: str = Query(..., description="ID d'utilisateur à rechercher"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Rechercher des paramètres par user_id (admin uniquement)"""
    try:
        service = SettingsService()
        return await service.search_by_user_id(user_id, skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=SettingsResponse)
async def get_settings(id: str, current_user: dict = Depends(get_current_user)):
    """Récupérer des paramètres par leur ID"""
    try:
        service = SettingsService()
        result = await service.get_by_id(id)
        if not result:
            raise HTTPException(status_code=404, detail="Paramètres non trouvés")
        if result.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à ces paramètres")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", response_model=SettingsResponse)
async def get_settings_by_user(user_id: str, current_user: dict = Depends(get_current_user)):
    """Récupérer les paramètres d'un utilisateur"""
    try:
        if user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé aux paramètres de cet utilisateur")
        service = SettingsService()
        result = await service.get_by_user_id(user_id)
        if not result:
            raise HTTPException(status_code=404, detail="Paramètres non trouvés pour cet utilisateur")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[SettingsResponse], dependencies=[Depends(get_current_admin)])
async def get_all_settings():
    """Récupérer tous les paramètres (admin uniquement)"""
    try:
        service = SettingsService()
        return await service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}", response_model=SettingsResponse)
async def update_settings(id: str, settings_update: SettingsUpdate, current_user: dict = Depends(get_current_user)):
    """Mettre à jour des paramètres"""
    try:
        service = SettingsService()
        settings = await service.get_by_id(id)
        if not settings:
            raise HTTPException(status_code=404, detail="Paramètres non trouvés")
        if settings.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à ces paramètres")
        result = await service.update(id, settings_update)
        if not result:
            raise HTTPException(status_code=404, detail="Paramètres non trouvés")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
async def delete_settings(id: str, current_user: dict = Depends(get_current_user)):
    """Supprimer des paramètres"""
    try:
        service = SettingsService()
        settings = await service.get_by_id(id)
        if not settings:
            raise HTTPException(status_code=404, detail="Paramètres non trouvés")
        if settings.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à ces paramètres")
        result = await service.delete(id)
        if not result:
            raise HTTPException(status_code=404, detail="Paramètres non trouvés")
        return {"message": "Paramètres supprimés avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))