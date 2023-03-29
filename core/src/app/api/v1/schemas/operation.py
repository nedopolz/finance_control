from src.app.api.v1.schemas.camel_model import CamelModel


class OperationSchema(CamelModel):
    id: int
    code: str
    name: str


class CreateOperationSchema(CamelModel):
    amount: float
    category_id: int
    account_id: int
    datetime: str
    type_id: int
