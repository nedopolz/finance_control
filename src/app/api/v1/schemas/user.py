from src.app.api.v1.schemas.camel_model import CamelModel


class UserSchema(CamelModel):
    external_id: str
