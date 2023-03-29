from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette import status

from src.app.api.v1.dependencies import get_current_user
from src.app.api.v1.schemas.operation import CreateOperationSchema
from src.app.api.v1.services.services import get_operation_service

router = APIRouter()


@router.post(
    "/",
    description="Создать Операцию",
    responses={status.HTTP_200_OK: {"operation_id": "id"}},
)
async def create_operation(
        operation: CreateOperationSchema,
        current_user=Depends(get_current_user),
        operation_service=Depends(get_operation_service),
):
    data = operation.dict()
    id = await operation_service.create_operation(data, current_user.id)
    return JSONResponse({"operation_id": id})
