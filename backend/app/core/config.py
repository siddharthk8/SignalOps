import os

from dotenv import load_dotenv

load_dotenv()

AI_MODEL_ID: str = os.environ["AWS_AI_MODEL_ID"]
SQLALCHEMY_DB_URL: str = os.environ["SQLALCHEMY_DB_URL"]
AWS_MODEL_RETRY_ATTEMPTS: int = 3
