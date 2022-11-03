from pydantic.main import BaseModel
from pydantic import EmailStr
from humps import camelize
from typing import Optional


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class UserOut(CamelModel):
    user_id: int
    first_name: str
    last_name: str
    patronymic: str
    email: str


class UserCreate(CamelModel):
    first_name: str
    last_name: str
    patronymic: str
    email: EmailStr
    password: str


class AddDevice(CamelModel):
    uid: int


class UserOptional(UserCreate):
    __annotations__ = {k: Optional[v] for k, v in UserCreate.__annotations__.items()}


class UserLogin(UserCreate):
    __annotations__ = {
        k: v
        for k, v in UserCreate.__annotations__.items()
        if k not in ("first_name", "last_name", "patronymic")
    }
