import logging
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_password_reset_email(email_to: str, token: str) -> None:
        project_name = settings.PROJECT_NAME
                                                                         
        reset_link = f"http://localhost:8000/reset-password?token={token}"
        
        message_content = f
                         
        logger.info(f"ENVIANDO CORREO DE RECUPERACIÓN A: {email_to}")
        logger.info(f"CONTENIDO:\n{message_content}")
        
                                                                      
        pass

email_service = EmailService()
