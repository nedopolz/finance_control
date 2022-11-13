from humps import camelize
from pydantic.main import BaseModel


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class Status(CamelModel):
    # id: int
    status_code: str
    # name: str


