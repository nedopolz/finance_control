from src.app.api.v1.schemas.account import CamelModel


class CurrencySchema(CamelModel):
    id: int
    code: str
    name: str
    symbol: str
