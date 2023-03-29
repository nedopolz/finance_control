from src.app.api.v1.schemas.camel_model import CamelModel


class StatusSchema(CamelModel):
    id: int
    code: str
    name: str
