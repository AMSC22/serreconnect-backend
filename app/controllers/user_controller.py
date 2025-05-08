from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Dict
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.auth.jwt_handler import get_current_admin

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate) -> UserResponse:
    """Créer un nouvel utilisateur (admin uniquement)"""
    try:
        service = UserService()
        result = await service.create(user)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/count", response_model=Dict[str, int], dependencies=[Depends(get_current_admin)])
async def count_users():
    """Compter les utilisateurs par rôle (admin uniquement)"""
    try:
        service = UserService()
        return await service.count_by_role()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=List[UserResponse], dependencies=[Depends(get_current_admin)])
async def search_users_by_email(
    email: str = Query(..., description="Email à rechercher"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Rechercher des utilisateurs par email (admin uniquement)"""
    try:
        service = UserService()
        return await service.search_by_email(email, skip, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=UserResponse, dependencies=[Depends(get_current_admin)])
async def get_user(id: str):
    """Récupérer un utilisateur par son ID (admin uniquement)"""
    try:
        service = UserService()
        result = await service.get_by_id(id)
        if not result:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[UserResponse], dependencies=[Depends(get_current_admin)])
async def get_all_users():
    """Récupérer tous les utilisateurs (admin uniquement)"""
    try:
        service = UserService()
        return await service.get_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}", response_model=UserResponse, dependencies=[Depends(get_current_admin)])
async def update_user(id: str, user_update: UserUpdate):
    """Mettre à jour un utilisateur (admin uniquement)"""
    try:
        service = UserService()
        result = await service.update(id, user_update)
        if not result:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}", dependencies=[Depends(get_current_admin)])
async def delete_user(id: str):
    """Supprimer un utilisateur (admin uniquement)"""
    try:
        service = UserService()
        result = await service.delete(id)
        if not result:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return {"message": "Utilisateur supprimé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    