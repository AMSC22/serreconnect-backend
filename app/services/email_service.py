import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

async def send_reset_password_email(to_email: str, reset_url: str):
    """Envoyer un e-mail de réinitialisation de mot de passe"""
    try:
        # Configurer les paramètres SMTP (par exemple, Gmail)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "your_email@gmail.com"
        sender_password = "your_app_password"

        # Créer le message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = "Réinitialisation de votre mot de passe"

        body = f"""
        Bonjour,

        Cliquez sur le lien suivant pour réinitialiser votre mot de passe :
        {reset_url}

        Ce lien expire dans 1 heure.

        Si vous n'avez pas demandé cette réinitialisation, ignorez cet e-mail.

        Cordialement,
        L'équipe SmartGreenhouse
        """
        message.attach(MIMEText(body, "plain"))

        # Envoyer l'e-mail
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, message.as_string())

        logger.info(f"E-mail de réinitialisation envoyé à {to_email}")
    except Exception as e:
        logger.error(f"Erreur lors de l'envoi de l'e-mail: {str(e)}")
        raise