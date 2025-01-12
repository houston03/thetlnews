from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    DATABASE_URL: str
    SECRET_KEY: str
    EMAIL_SENDER: str
    EMAIL_PASSWORD: str
    SMTP_SERVER: str = "smtp.yandex.com"
    SMTP_PORT: int = 587
    ALGORITHM: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str


settings = Settings()

