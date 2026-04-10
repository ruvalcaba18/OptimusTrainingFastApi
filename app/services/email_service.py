import logging
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailService:
    @staticmethod
    def send_password_reset_email(email_to: str, token: str) -> None:
        project_name = settings.PROJECT_NAME
                                                                         
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"
        
        message_content = f"""
        Hola,
        Has solicitado restablecer tu contraseña para {project_name}.
        Usa el siguiente enlace para crear una nueva contraseña: {reset_link}
        
        Si no solicitaste esto, simplemente ignora este correo.
        """
        
                                  
        logger.info(f"ENVIANDO CORREO DE RECUPERACIÓN A: {email_to}")
        logger.info(f"CONTENIDO:\n{message_content}")
        
                                                                      
        pass

email_service = EmailService()
