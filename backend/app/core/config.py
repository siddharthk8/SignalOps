from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", env_file_encoding="utf-8")

    sqlalchemy_db_url: str
    aws_ai_model_id: str
    aws_ai_model_retry_attempts: int = 3


settings = Settings()  # type: ignore[call-arg]
