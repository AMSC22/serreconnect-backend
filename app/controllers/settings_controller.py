from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict, Optional
from app.services.settings_service import SettingsService
from app.schemas.settings_schema import SettingsCreate, SettingsUpdate, SettingsResponse
from app.auth.jwt_handler import get_current_user, get_current_admin
from datetime import datetime

router = APIRouter(
    prefix="/settings",
    tags=["settings"]
)

@router.post("/", response_model=SettingsResponse)
async def create_settings(settings: SettingsCreate, current_user: dict = Depends(get_current_user)):
    """Créer de nouveaux paramètres"""
    try:
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
async def get_settings_by_user(user_id: str, greenhouse_id: Optional[str] = None, current_user: dict = Depends(get_current_user)):
    """Récupérer les paramètres d'une serre d'un utilisateur"""
    try:
        query = {"user_id": user_id}
        if greenhouse_id:
            query["greenhouse_id"] = greenhouse_id
        service = SettingsService()
        result = await service.get_by_user_id(query)
        if not result:
            raise HTTPException(status_code=404, detail="Paramètres non trouvés pour cet utilisateur")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/greenhouse/{user_id}", response_model=SettingsResponse)
async def get_settings_by_greenhouse_id(user_id: str, greenhouse_id: str, current_user: dict = Depends(get_current_user)):
    """Récupérer les paramètres d'une serre d'une serre"""
    try:
        if user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé aux paramètres de cette serre")
        query = {"user_id": user_id, "greenhouse_id": greenhouse_id}
        service = SettingsService()
        result = await service.get_by_greenhouse_id(query)
        if not result:
            result = await service.get_default_settings()
            result["user_id"] = user_id
            result["greenhouse_id"] = greenhouse_id
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

@router.put("/admin/{id}", response_model=SettingsResponse)
async def update_settings_admin(id: str, settings_update: SettingsUpdate, current_user: dict = Depends(get_current_admin)):
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

@router.put("/user/{id}", response_model=SettingsResponse)
async def update_settings_user(id: str, settings_update: SettingsUpdate, current_user: dict = Depends(get_current_user)):
    """Mettre à jour des paramètres"""
    try:
        service = SettingsService()
        result = await service.update(id, settings_update)
        if not result:
            raise HTTPException(status_code=404, detail="Paramètres non trouvé")
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
    
@router.get("/default/", response_model=SettingsResponse)
async def get_default_settings(current_user: Dict = Depends(get_current_user)):
    """Récupérer les paramètres par défaut"""
    try:
        service = SettingsService()
        settings = await service.get_default_settings()
        if not settings:
            raise HTTPException(status_code=404, detail="Paramètres par défaut non trouvés")
        return settings
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des paramètres par défaut dans controller: {str(e)}")

@router.put("/default", response_model=SettingsResponse)
async def update_default_settings(settings_update: SettingsUpdate, current_user: Dict = Depends(get_current_admin)):
    """Mettre à jour les paramètres par défaut (admin uniquement)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Seul un administrateur peut modifier les paramètres par défaut")
    try:
        service = SettingsService()
        default_settings = await service.get_default_settings()
        if not default_settings:
            raise HTTPException(status_code=404, detail="Paramètres par défaut non trouvés")
        
        # Mettre à jour les champs non nuls
        update_data = settings_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.now()
        
        # Mettre à jour dans la base
        result = await service.repository.collection.update_one(
            {"is_default": True},
            {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Aucune modification appliquée")
        
        updated_settings = await service.get_default_settings()
        return updated_settings
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour des paramètres par défaut: {str(e)}")