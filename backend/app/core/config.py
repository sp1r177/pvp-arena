from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

    APP_ENV: str = "dev"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    BACKEND_CORS_ORIGINS: str = "http://localhost:5173,https://vk.com,https://*.github.io,https://*.githubusercontent.com,https://sp1r177.github.io"

    DATABASE_URL: str

    JWT_SECRET: str
    JWT_ALG: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    VK_APP_ID: int
    VK_SERVICE_KEY: str | None = None

    # Game
    TICK_RATE: int = 20
    ROOM_CAPACITY_FFA: int = 12
    ROOM_CAPACITY_DUO: int = 4
    BOT_FILL: bool = True
    BOT_SKILL: float = 0.6
    MATCH_DURATION_SEC: int = 150

    @property
    def cors_origins(self) -> List[str]:
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()  # global singleton for simple access