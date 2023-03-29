from fastapi import HTTPException
from humps import camelize
from pydantic import Field
from pydantic.main import BaseModel
from starlette import status


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class ErrorMessage(CamelModel):
    message: str = Field(description="Сообщение об ошибке")


unauthorised_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Не авторизован",
    headers={"WWW-Authenticate": "Bearer"},
)
credentials_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

invalid_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has been expired.",
    headers={"WWW-Authenticate": "Bearer"},
)

responses_exceptions = {
    credentials_exception.status_code: {"model": ErrorMessage},
    unauthorised_exception.status_code: {"model": ErrorMessage},
}
