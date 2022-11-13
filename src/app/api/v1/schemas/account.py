from humps import camelize
from pydantic.main import BaseModel

from src.app.api.v1.schemas.currency import Currency
from src.app.api.v1.schemas.status import Status
from src.app.api.v1.schemas.type import Type


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class Account(CamelModel):
    id: int
    status: Status | None
    # type: Type
    # currency: Currency


class CreateAccount(CamelModel):
    type_id: int
    currency_id: int
