from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, EmailStr

load_dotenv()


class Settings(BaseSettings):
    app_title: str = "Сервис"
    database_url: str = "sqlite+aiosqlite:///./charityfund.db"
    secret: str = "SECRET"
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    model_config = {
        'env_file': '.env',
        'env_file_encoding': 'utf-8',
    }

settings = Settings()  # type: ignore
