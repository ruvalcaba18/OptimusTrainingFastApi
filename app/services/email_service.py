"""
Email service - handles sending emails (mocked for development).
"""
import logging
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_password_reset_email(email_to: str, token: str) -> None:
        """
        Sends a password reset email. In development, it just logs the token.
        """
        project_name = settings.PROJECT_NAME
        # In a real app, this would be a link to your frontend reset page
        reset_link = f"http://localhost:8000/reset-password?token={token}"
        
        message_content = f"""
        Hola,
        Has solicitado restablecer tu contraseña para {project_name}.
        Usa el siguiente enlace para crear una nueva contraseña: {reset_link}
        
        Si no solicitaste esto, simplemente ignora este correo.
        """
        
        # Mocking the send process
        logger.info(f"ENVIANDO CORREO DE RECUPERACIÓN A: {email_to}")
        logger.info(f"CONTENIDO:\n{message_content}")
        
        # Here you would use libraries like 'emails' or 'fastapi-mail'
        pass

email_service = EmailService()
