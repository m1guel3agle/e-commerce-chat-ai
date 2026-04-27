from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración global de la aplicación.
    Lee los valores desde el archivo .env automáticamente.
    """
    GEMINI_API_KEY: str = ""
    DATABASE_URL: str = "sqlite:///./data/ecommerce_chat.db"
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()