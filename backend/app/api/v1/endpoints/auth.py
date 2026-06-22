from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.core import get_db
from app.domains.auth import service
from app.domains.auth.schemas import TokenResponse

router = APIRouter()


@router.post("/token", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def create_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    return await service.create_token(form_data, db)
