from src.app.api.v1.schemas.account import CamelModel


class OperationSchema(CamelModel):
    id: int
    code: str
    name: str