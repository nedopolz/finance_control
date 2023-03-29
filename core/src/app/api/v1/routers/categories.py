from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.api.v1.dependencies import get_current_user, get_session
from src.app.api.v1.schemas.сategory import CategorySchema, CreateCategorySchema
from src.app.api.v1.services.DBservices import get_categoryDB_service
from src.app.api.v1.services.services import get_category_service

router = APIRouter()


@router.get("/", description="Получить список категорий пользователя", response_model=List[CategorySchema])
async def get_categories(
        current_user=Depends(get_current_user),
        category_service=Depends(get_categoryDB_service),
        session: AsyncSession = Depends(get_session)
):
    category = await category_service.get_category_by_user_id(current_user.id, session)
    return category


@router.post(
    "/",
    description="Создать Категорию",
    responses={status.HTTP_200_OK: {"category_id": "id"}},
)
async def create_category(
        category: CreateCategorySchema,
        current_user=Depends(get_current_user),
        category_service=Depends(get_category_service),
):
    data = category.dict()
    data["user_id"] = current_user.id
    id = await category_service.create_category(data)
    return JSONResponse({"category_id": id})


@router.delete(
    "/{category_id}",
    description="Удалить Категорию",
    responses={status.HTTP_200_OK: {"status": "ok"}, status.HTTP_404_NOT_FOUND: {"status": "not found"}},
)
async def delete_category(
        category_id: int,
        current_user=Depends(get_current_user),
        category_service=Depends(get_category_service),
):
    category = await category_service.delete_category(category_id, current_user.id)
    if category:
        return JSONResponse({"status": "ok"})
    return JSONResponse({"status": "not found"}, status_code=status.HTTP_404_NOT_FOUND)
