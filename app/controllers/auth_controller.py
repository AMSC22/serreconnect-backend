from fastapi import APIRouter, HTTPException, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.services.user_service import UserService
from app.services.session_service import SessionService
from app.schemas.session_schema import SessionCreate
from app.schemas.user_schema import UserUpdate, UserResponse
from app.auth.jwt_handler import create_access_token, get_current_user
from app.services.email_service import send_reset_password_email
import secrets
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
    
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
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": user.is_admin,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat(),
                "updated_at": user.updated_at.isoformat()
            }
        }
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

@router.post("/forgot-password")
async def forgot_password(email: str = Form(...)):
    """Envoyer un lien de réinitialisation de mot de passe"""
    try:
        user_service = UserService()
        user = await user_service.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        reset_token = secrets.token_urlsafe(32)
        # Stocker le token dans la base de données (expire après 1 heure)
        await user_service.update(user.id, UserUpdate(reset_token=reset_token))
        reset_url = f"http://localhost:3000/reset-password?token={reset_token}&email={email}"
        await send_reset_password_email(email, reset_url)
        return {"message": "E-mail de réinitialisation envoyé"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset-password")
async def reset_password(
    token: str = Form(...),
    email: str = Form(...),
    new_password: str = Form(...)
):
    """Réinitialiser le mot de passe"""
    try:
        user_service = UserService()
        user = await user_service.get_by_email(email)
        if not user or user.reset_token != token:
            raise HTTPException(status_code=400, detail="Token invalide")
        # Réinitialiser le mot de passe et supprimer le token
        await user_service.update(user.id, UserUpdate(password=new_password, reset_token=None))
        return {"message": "Mot de passe réinitialisé avec succès"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/me", response_model=UserResponse)
async def get_current_user_data(current_user: dict = Depends(get_current_user)):
    """Récupérer les données de l'utilisateur actuel"""
    try:
        user_service = UserService()
        user = await user_service.get_by_id(current_user["user_id"])
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erreur lors de la récupération de l'utilisateur: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur interne du serveur")

@router.patch("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: UserResponse = Depends(get_current_user)
):
    user_service = UserService()
    updated_user = await user_service.update(current_user.id, user_update)
    if not updated_user:
        raise HTTPException(status_code=400, detail="Échec de la mise à jour du profil")
    return updated_user