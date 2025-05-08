from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.services.actuator_service import ActuatorService
from app.schemas.actuator_schema import ActuatorCreate, ActuatorUpdate, ActuatorResponse
from app.auth.jwt_handler import get_current_user

router = APIRouter(
    prefix="/actuators",
    tags=["actuators"]
)

@router.post("/", response_model=ActuatorResponse)
async def create_actuator(actuator: ActuatorCreate, current_user: dict = Depends(get_current_user)):
    """Créer un nouvel actionneur"""
    try:
        service = ActuatorService()
        result = await service.create(actuator)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/greenhouse/{greenhouse_id}", response_model=List[ActuatorResponse])
async def get_actuators_by_greenhouse(greenhouse_id: str, current_user: dict = Depends(get_current_user)):
    """Récupérer les actionneurs d'une serre"""
    try:
        service = ActuatorService()
        return await service.get_by_greenhouse_id(greenhouse_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}", response_model=ActuatorResponse)
async def update_actuator(id: str, actuator_update: ActuatorUpdate, current_user: dict = Depends(get_current_user)):
    """Mettre à jour un actionneur"""
    try:
        service = ActuatorService()
        result = await service.update(id, actuator_update)
        if not result:
            raise HTTPException(status_code=404, detail="Actionneur non trouvé")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{id}")
async def delete_actuator(id: str, current_user: dict = Depends(get_current_user)):
    """Supprimer un actionneur"""
    try:
        service = ActuatorService()
        result = await service.delete(id)
        if not result:
            raise HTTPException(status_code=404, detail="Actionneur non trouvé")
        return {"message": "Actionneur supprimé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))