from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.v1.schemas.user import User
from src.app.api.v1.services.services import get_user_service
from src.app.db import async_session


async def get_current_user(
    user: User,
    user_service=Depends(get_user_service),
):
    user = await user_service.get_user_by_external_id(user.external_id)
    return user


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

