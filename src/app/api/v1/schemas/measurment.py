from datetime import datetime

from humps import camelize
from pydantic.main import BaseModel


class CamelModel(BaseModel):
    class Config:
        alias_generator = camelize
        allow_population_by_field_name = True


class Measurement(CamelModel):
    measurement_value: float
    time: datetime
