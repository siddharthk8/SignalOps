from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
    )

    secret_key: SecretStr
    sqlalchemy_db_url: SecretStr
    password_hash_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    aws_ai_model_id: str
    aws_ai_model_retry_attempts: int = 3


settings = Settings()  # type: ignore[call-arg]
