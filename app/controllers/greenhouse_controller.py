from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from app.services.greenhouse_service import GreenhouseService
from app.schemas.greenhouse_schema import GreenhouseCreate, GreenhouseUpdate, GreenhouseResponse
from app.auth.jwt_handler import get_current_user

router = APIRouter(
    prefix="/greenhouses",
    tags=["greenhouses"]
)

@router.post("/", response_model=GreenhouseResponse)
async def create_greenhouse(greenhouse: GreenhouseCreate, current_user: dict = Depends(get_current_user)):
    """Créer une nouvelle serre"""
    try:
        if greenhouse.user_id != current_user["user_id"]:
            raise HTTPException(status_code=403, detail="Vous ne pouvez créer une serre que pour votre propre utilisateur")
        service = GreenhouseService()
        result = await service.create(greenhouse)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=GreenhouseResponse)
async def get_greenhouse(id: str, current_user: dict = Depends(get_current_user)):
    """Récupérer une serre par son ID"""
    try:
        service = GreenhouseService()
        result = await service.get_by_id(id)
        if not result:
            raise HTTPException(status_code=404, detail="Serre non trouvée")
        if result.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette serre")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", response_model=List[GreenhouseResponse])
async def get_greenhouses_by_user(user_id: str, current_user: dict = Depends(get_current_user)):
    """Récupérer les serres d'un utilisateur"""
    try:
        if user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé aux serres de cet utilisateur")
        service = GreenhouseService()
        return await service.get_by_user_id(user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=List[GreenhouseResponse])
async def search_greenhouses(
    name: str = Query(..., description="Nom de la serre à rechercher"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user)
):
    """Rechercher des serres par nom"""
    try:
        service = GreenhouseService()
        results = await service.search_by_name(name, skip, limit)
        # Filtrer les résultats pour les non-admins
        if not current_user["is_admin"]:
            results = [r for r in results if r.user_id == current_user["user_id"]]
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[GreenhouseResponse])
async def get_all_greenhouses(current_user: dict = Depends(get_current_user)):
    """Récupérer toutes les serres (admins uniquement)"""
    try:
        if not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
        service = GreenhouseService()
        return await service.get_all()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}", response_model=GreenhouseResponse)
async def update_greenhouse(id: str, greenhouse_update: GreenhouseUpdate, current_user: dict = Depends(get_current_user)):
    """Mettre à jour une serre"""
    try:
        service = GreenhouseService()
        greenhouse = await service.get_by_id(id)
        if not greenhouse:
            raise HTTPException(status_code=404, detail="Serre non trouvée")
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette serre")
        result = await service.update(id, greenhouse_update)
        if not result:
            raise HTTPException(status_code=404, detail="Serre non trouvée")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
async def delete_greenhouse(id: str, current_user: dict = Depends(get_current_user)):
    """Supprimer une serre"""
    try:
        service = GreenhouseService()
        greenhouse = await service.get_by_id(id)
        if not greenhouse:
            raise HTTPException(status_code=404, detail="Serre non trouvée")
        if greenhouse.user_id != current_user["user_id"] and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Accès non autorisé à cette serre")
        result = await service.delete(id)
        if not result:
            raise HTTPException(status_code=404, detail="Serre non trouvée")
        return {"message": "Serre supprimée avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))