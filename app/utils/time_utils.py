from datetime import datetime
import pytz
from app.config.settings import settings

def get_local_time() -> datetime:
    """Retourner la date et l'heure actuelles dans le fuseau horaire configuré"""
    settings.TIMEZONE = "Europe/Paris"
    tz = pytz.timezone(settings.TIMEZONE)
    return datetime.now(tz)

def convert_to_local_time(dt: datetime) -> datetime:
    """Convertir un timestamp UTC en heure locale"""
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    tz = pytz.timezone(settings.TIMEZONE)
    return dt.astimezone(tz)