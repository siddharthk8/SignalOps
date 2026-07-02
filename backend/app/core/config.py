from pathlib import Path
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / "backend/.env",
        env_file_encoding="utf-8",
    )

    secret_key: SecretStr
    database_url: SecretStr
    password_hash_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    source_apps_per_page: int = 10
    batches_per_page: int = 10

    # Redis configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str | None = None

    # Testing environment
    testing: bool = False

    # development/production environment
    env: Literal["development"] | Literal["production"] = "development"

    # forgot password email configuration
    mail_from: str
    password_reset_request_cooldown_seconds: int = 120
    reset_token_expire_minutes: int = 30

    frontend_url: str = "http://localhost:8000"

    # Optional AWS credentials.
    # If not provided, boto3 falls back to its default credential chain:
    # environment variables, shared AWS config (~/.aws/credentials),
    # IAM roles (EC2/ECS/Lambda), etc.
    aws_access_key_id: SecretStr | None = None
    aws_secret_access_key: SecretStr | None = None

    # Bedrock configuration
    bedrock_region: str = "ap-south-1"
    bedrock_model_id: str
    bedrock_model_retry_attempts: int = 3

    # S3 configuration
    s3_region: str = "ap-south-1"
    s3_bucket_name: str
    max_upload_size_bytes: int = 5 * 1024 * 1024  # 5 MB

    # SES configuration
    ses_region: str = "ap-south-1"


settings = Settings()  # type: ignore[call-arg]
