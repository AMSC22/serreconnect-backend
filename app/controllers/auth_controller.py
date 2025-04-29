from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.services.user_service import UserService
from app.services.session_service import SessionService
from app.schemas.session_schema import SessionCreate
from app.auth.jwt_handler import create_access_token, get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authentifier un utilisateur et générer un JWT"""
    try:
        user_service = UserService()
        user = await user_service.get_by_email(form_data.username)  # username = email
        if not user:
            raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
        
        # Vérifier le mot de passe
        if not user_service.pwd_context.verify(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
        
        # Créer une session
        session_service = SessionService()
        session_data = SessionCreate(user_id=user.id, session_id="", is_active=True)  # session_id sera généré
        session = await session_service.create(session_data)
        
        # Générer le JWT
        access_token = create_access_token(data={
            "sub": user.id,
            "session_id": session.session_id,
            "is_admin": user.is_admin
        })
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de l'authentification: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Invalider la session actuelle"""
    try:
        session_service = SessionService()
        result = await session_service.invalidate_session(current_user["session_id"])
        if not result:
            raise HTTPException(status_code=404, detail="Session non trouvée")
        return {"message": "Déconnexion réussie"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la déconnexion: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")