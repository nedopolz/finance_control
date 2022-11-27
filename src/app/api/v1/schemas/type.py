from src.app.api.v1.schemas.account import CamelModel


class TypeSchema(CamelModel):
    id: int
    code: str
    name: str
