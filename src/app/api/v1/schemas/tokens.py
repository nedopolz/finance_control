from pydantic.main import BaseModel
from humps import camelize
from typing import Optional


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class Token(CamelModel):
    access_token: str
    token_type: str


class TokenData(CamelModel):
    user_id: int
    email: Optional[str] = None
