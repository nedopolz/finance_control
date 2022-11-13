from humps import camelize
from pydantic.main import BaseModel


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class Type(CamelModel):
    id: int
    code: str
    name: str

