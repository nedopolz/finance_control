from src.app.api.v1.schemas.account import CamelModel


class UserSchema(CamelModel):
    external_id: str
