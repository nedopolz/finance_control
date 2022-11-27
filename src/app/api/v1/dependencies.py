from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.v1.schemas.user import UserSchema
from src.app.api.v1.services.DBservices import get_userDB_service
from src.app.db import async_session


async def get_current_user(
    user: UserSchema,
    user_service=Depends(get_userDB_service),
):
    user = await user_service.get_user_by_external_id(user.external_id)
    return user


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
