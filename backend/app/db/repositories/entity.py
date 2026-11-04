from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.entity import Entity as ORMEntity
from app.schemas.entity import Entity


class EntityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _check_exists(self, entity_payload: dict[str, Any]):
        query = await self.db.execute(
            select(ORMEntity).where(
                ORMEntity.user == entity_payload.get("user"),
                ORMEntity.email == entity_payload.get("email"),
                ORMEntity.ip_address == entity_payload.get("ip_address"),
                ORMEntity.session_id == entity_payload.get("session_id"),
                ORMEntity.token_id == entity_payload.get("token_id"),
                ORMEntity.request_id == entity_payload.get("request_id"),
            )
        )
        result = query.scalar_one_or_none()
        return result

    async def save(self, entity: Entity, batch_id: int) -> ORMEntity:
        entity_payload = entity.model_dump(exclude={"id", "ip_address"})
        if entity.ip_address:
            entity_payload["ip_address"] = str(entity.ip_address)

        entity_payload["batch_id"] = batch_id
        pre_existing_entity = await self._check_exists(entity_payload)
        if pre_existing_entity is not None:
            return pre_existing_entity

        e = ORMEntity(**entity_payload)
        self.db.add(e)
        await self.db.flush()
        return e
