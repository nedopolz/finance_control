from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from starlette import status

from src.app.security import create_access_token, create_refresh_token, get_current_user
from src.app.api.v1.services.services import get_auth_service
from src.app.api.v1.schemas.exceptions import ErrorMessage
from src.app.api.v1.schemas.user import UserCreate, UserOut

router = APIRouter()


@router.post(
    "/signup",
    description="Регистрация пользователя",
    responses={
        status.HTTP_201_CREATED: {"model": UserOut},
        status.HTTP_409_CONFLICT: {"model": ErrorMessage},
    },
)
async def sign_up(data: UserCreate, auth_service=Depends(get_auth_service)):
    user = await auth_service.find_by_email(data.email)
    if user:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorMessage(message="Юзер c таким email уже существует.").dict(),
        )
    else:
        return await auth_service.signup_user(data)


@router.post(
    "/patient-signup",
    description="Регистрация пациента",
    responses={
        status.HTTP_201_CREATED: {"model": UserOut},
        status.HTTP_409_CONFLICT: {"model": ErrorMessage},
    },
)
async def patient_sign_up(
        data: UserCreate,
        auth_service=Depends(get_auth_service),
        current_user=Depends(get_current_user),
):
    user = await auth_service.find_by_email(data.email)
    if user:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=ErrorMessage(message="Юзер c таким email уже существует.").dict(),
        )
    else:
        patient = await auth_service.signup_user(data)
        await auth_service.create_user_patient_map(
            doctor_id=current_user.user_id, patient_id=patient.user_id
        )
        return patient


@router.post(
    "/login", description="Вход в систему. Тут получаются access и refresh токены."
)
async def login(
        request: OAuth2PasswordRequestForm = Depends(),
        auth_service=Depends(get_auth_service),
):
    user = await auth_service.find_by_email(email=request.username)
    if not user or not auth_service.verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Credentials"
        )

    # Generate a JWT Tokens
    access_token = create_access_token(data={"sub": user.email, "id": user.user_id})
    refresh_token = create_refresh_token(data={"sub": user.email, "id": user.user_id})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
