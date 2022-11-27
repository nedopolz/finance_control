from src.app.api.v1.schemas.camel_model import CamelModel
from src.app.api.v1.schemas.currency import CurrencySchema
from src.app.api.v1.schemas.status import StatusSchema
from src.app.api.v1.schemas.type import TypeSchema


class AccountSchema(CamelModel):
    id: int
    Status: StatusSchema
    AccountType: TypeSchema
    Currency: CurrencySchema


class CreateAccount(CamelModel):
    type_id: int
    currency_id: int
