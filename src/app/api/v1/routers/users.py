import datetime
import io
from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from starlette import status

from src.app.api.v1.dependencies import paginator
from src.app.api.v1.schemas.exceptions import ErrorMessage
from src.app.api.v1.schemas.user import UserOut, UserOptional, AddDevice
from src.app.api.v1.services.services import get_auth_service, get_device_service
from src.app.security import get_current_user

router = APIRouter()


@router.get(
    "/",
    description="Получить всех юзеров. И врачей, и пациентов.",
    responses={status.HTTP_200_OK: {"model": List[UserOut]}},
)
async def users(auth_service=Depends(get_auth_service), page=Depends(paginator)):
    return await auth_service.get_users(page)


@router.get(
    "/patients", description="Получить всех пациентов, привязанных текущему врачу."
)
async def patients(
        auth_service=Depends(get_auth_service),
        current_user=Depends(get_current_user),
        page=Depends(paginator),
):
    return await auth_service.get_patients(user_id=current_user.user_id, page=page)


@router.get(
    "/{user_id}",
    description="Получить юзера по id",
    responses={status.HTTP_200_OK: {"model": UserOut}},
)
async def user_by_id(user_id: int, auth_service=Depends(get_auth_service)):
    user = await auth_service.get_by_id(user_id)
    return (
        UserOut(**user)
        if user
        else JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorMessage(message="Юзера с таким id не существует.").dict(),
        )
    )


@router.patch(
    "/{user_id}",
    description="Изменить данные",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_409_CONFLICT: {"model": ErrorMessage},
    },
)
async def change_credentials(
        user_id: int, data: UserOptional, auth_service=Depends(get_auth_service)
):
    if data.email:
        emails_exists = await auth_service.find_by_email(data.email)
        if emails_exists:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content=ErrorMessage(
                    message="Юзер c таким email уже существует."
                ).dict(),
            )
        else:
            return await auth_service.change_credentials(user_id, data)
    return await auth_service.change_credentials(user_id, data)


@router.delete(
    "/{user_id}",
    description="Удалить пользователя по id",
    responses={
        status.HTTP_204_NO_CONTENT: {"model": None},
        status.HTTP_404_NOT_FOUND: {"model": ErrorMessage},
    },
)
async def user(user_id: int, auth_service=Depends(get_auth_service)):
    exists = await auth_service.get_by_id(user_id)
    if not exists:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorMessage(message="Такого пользователя не существует.").dict(),
        )
    else:
        return await auth_service.delete_user(user_id)


@router.get("/export/{user_id}", description="Скачать csv файл.")
async def export(
        user_id: int,
        current_user=Depends(get_current_user),
        auth_service=Depends(get_auth_service),
):
    user = await auth_service.get_by_id(user_id)
    df = pandas.DataFrame(UserOut(**user).dict(), index=[0])
    stream = io.StringIO()
    df.to_csv(stream, index=False, sep=";")
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")

    response.headers["Content-Disposition"] = (
        f"attachment;"
        f"filename={user.first_name}_"
        f"{user.last_name}_"
        f"{user.patronymic}_"
        f"{datetime.datetime.utcnow()}.csv"
    )

    return response


@router.post(
    "/add_device",
    description="Привязать устройство",
    responses={status.HTTP_200_OK: {"status": "ok"}},
)
async def add_device_to_user(
        data: AddDevice,
        current_user=Depends(get_current_user),
        device_service=Depends(get_device_service),
):
    if await device_service.add_user(current_user, data.uid):
        return JSONResponse({"status": "ok"})
    return JSONResponse({"status": "not ok"})
