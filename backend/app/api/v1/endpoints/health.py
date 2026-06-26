from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from app.db.core import DBSessionDep

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check(db: DBSessionDep):
    try:
        await db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database unavailable.",
        ) from exc

    return {"status": "healthy"}
