from celery import Celery
import smtplib
from email.mime.text import MIMEText
from src.app.core.config import settings
import logging

# Настройка логирования
logger = logging.getLogger(__name__)

# Инициализация Celery
celery = Celery(__name__, broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND)

@celery.task
def send_email(to_email: str, subject: str, message: str):
    """Отправка email с использованием SMTP с изменением имени отправителя."""
    try:
        # Указываем отображаемое имя отправителя
        display_name = "TheTL Support Team"
        sender = f"{display_name} <{settings.EMAIL_SENDER}>"

        # Подготовка MIME-сообщения
        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = sender  # Используем отображаемое имя
        msg["To"] = to_email

        # Настройка соединения с SMTP-сервером
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_SENDER, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_SENDER, [to_email], msg.as_string())

        logger.info(f"Email sent to {to_email} with subject: {subject}")
        return "Email sent successfully"
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        raise
# celery -A src.app.tasks.send_email worker --loglevel=INFO --pool=solo
# celery -A backend.src.app.tasks.celery_worker worker --loglevel=info
