from humps import camelize
from pydantic.main import BaseModel

from src.app.api.v1.schemas.currency import CurrencySchema
from src.app.api.v1.schemas.status import StatusSchema
from src.app.api.v1.schemas.type import TypeSchema


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True
        orm_mode = True


class AccountSchema(CamelModel):
    id: int
    Status: StatusSchema
    AccountType: TypeSchema
    Currency: CurrencySchema


class CreateAccount(CamelModel):
    type_id: int
    currency_id: int
