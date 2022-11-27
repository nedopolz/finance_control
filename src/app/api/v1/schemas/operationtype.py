from src.app.api.v1.schemas.camel_model import CamelModel


class OperationTypeSchema(CamelModel):
    id: int
    code: str
    name: str
