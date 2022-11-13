from humps import camelize
from pydantic.main import BaseModel

from src.app.api.v1.schemas.currency import Currency
from src.app.api.v1.schemas.status import StatusSchema
from src.app.api.v1.schemas.type import Type


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True
        orm_mode = True


class Account(CamelModel):
    id: int
    status: StatusSchema
    # type: Type
    # currency: Currency


class CreateAccount(CamelModel):
    type_id: int
    currency_id: int
