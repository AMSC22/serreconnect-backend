from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.config.settings import settings
from app.services.session_service import SessionService
from app.utils.time_utils import get_local_time
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def create_access_token(data: dict) -> str:
    """Créer un JWT avec une expiration et dernière activité"""
    to_encode = data.copy()
    expire = get_local_time() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "last_activity": get_local_time().isoformat()
    })
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Vérifier et décoder le JWT, et valider la session"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Impossible de valider les credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        session_id: str = payload.get("session_id")
        is_admin: bool = payload.get("is_admin", False)
        last_activity_str: str = payload.get("last_activity")
        if not all([user_id, session_id, last_activity_str]):
            raise credentials_exception

        # Vérifier la session dans MongoDB
        session_service = SessionService()
        session = await session_service.get_by_session_id(session_id)
        if not session or session.user_id != user_id or not session.is_active:
            raise credentials_exception

        # Vérifier le timeout d'inactivité
        last_activity = datetime.fromisoformat(last_activity_str)
        if (get_local_time() - last_activity).total_seconds() / 60 > settings.SESSION_INACTIVITY_TIMEOUT_MINUTES:
            await session_service.invalidate_session(session_id)
            raise HTTPException(status_code=401, detail="Session inactive, veuillez vous reconnecter")

        # Mettre à jour la dernière activité
        await session_service.update_last_activity(session_id)

        return {"user_id": user_id, "session_id": session_id, "is_admin": is_admin}
    except JWTError as e:
        logger.error(f"Erreur lors du décodage du JWT: {str(e)}")
        raise credentials_exception

async def get_current_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Vérifier que l'utilisateur est un admin"""
    if not current_user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Accès réservé aux administrateurs")
    return current_user