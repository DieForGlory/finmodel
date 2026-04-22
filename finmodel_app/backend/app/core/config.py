from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Real Estate FinModel API"
    DATABASE_URL: str = "sqlite:///./finmodel.db"

settings = Settings()