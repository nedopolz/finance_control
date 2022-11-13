from humps import camelize
from pydantic.main import BaseModel


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class User(CamelModel):
    external_id: str
