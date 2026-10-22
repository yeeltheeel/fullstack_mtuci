from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    DATABASE_URL: str = "postgresql+asyncpg://bookexchange:bookexchange@localhost:5432/bookexchange"
    SECRET_KEY: str = "SomeKey!1"
    ACCESS_TOKEN_EXPIRE_MIN: int = 60
    DEBUG: bool = True

settings = Settings()
