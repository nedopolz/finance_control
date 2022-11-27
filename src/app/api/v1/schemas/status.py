from src.app.api.v1.schemas.account import CamelModel


class StatusSchema(CamelModel):
    id: int
    code: str
    name: str
