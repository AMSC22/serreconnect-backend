from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from app.services.badge_service import BadgeService
from app.schemas.badge_schema import BadgeCreate, BadgeUpdate, BadgeResponse
from app.models.user_model import UserModel
from app.auth.jwt_handler import get_current_user, get_current_admin

router = APIRouter(
    prefix="/badges",
    tags=["badges"]
)

@router.post("/", response_model=BadgeResponse)
async def create_badge(
    badge: BadgeCreate,
    current_user: UserModel = Depends(get_current_user)
):
    """Créer un nouveau badge"""
    try:
        service = BadgeService()
        result = await service.create(badge, str(current_user["user_id"]))
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", response_model=List[BadgeResponse])
async def get_user_badges(
    user_id: str,
    current_user: UserModel = Depends(get_current_user)
):
    """Récupérer les badges d'un utilisateur"""
    try:
        if str(current_user["user_id"]) != user_id and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Non autorisé")
        service = BadgeService()
        result = await service.get_by_user_id(user_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/greenhouse/{user_id}", response_model=List[BadgeResponse])
async def get_greenhouse_badges(
    user_id: str,
    greenhouse_id: str,
    current_user: UserModel = Depends(get_current_user)
):
    """Récupérer les badges d'une serre d'un utilisateur"""
    try:
        if str(current_user["user_id"]) != user_id and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Non autorisé")
        service = BadgeService()
        result = await service.get_by_greenhouse_id(user_id, greenhouse_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=BadgeResponse)
async def get_badge(
    id: str,
    current_user: UserModel = Depends(get_current_user)
):
    """Récupérer un badge par son ID"""
    try:
        service = BadgeService()
        result = await service.get_by_id(id)
        if not result:
            raise HTTPException(status_code=404, detail="Badge non trouvé")
        if result.user_id != str(current_user["user_id"]) and not current_user["is_admin"]:
            raise HTTPException(status_code=403, detail="Non autorisé")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}", response_model=BadgeResponse)
async def update_badge(
    id: str,
    badge_update: BadgeUpdate,
    current_user: UserModel = Depends(get_current_user)
):
    """Mettre à jour un badge"""
    try:
        service = BadgeService()
        result = await service.update(id, badge_update, str(current_user["user_id"]))
        if not result:
            raise HTTPException(status_code=404, detail="Badge non trouvé")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}")
async def delete_badge(
    id: str,
    current_user: UserModel = Depends(get_current_user)
):
    """Supprimer un badge"""
    try:
        service = BadgeService()
        result = await service.delete(id, str(current_user["user_id"]))
        if not result:
            raise HTTPException(status_code=404, detail="Badge non trouvé")
        return {"message": "Badge supprimé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[BadgeResponse], dependencies=[Depends(get_current_admin)])
async def get_all_badges(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Récupérer tous les badges (admin uniquement)"""
    try:
        service = BadgeService()
        return await service.get_all(skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))