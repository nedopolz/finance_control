from typing import List

from src.app.api.v1.schemas.camel_model import CamelModel
from src.app.api.v1.schemas.operationtype import OperationTypeSchema


class CategorySchema(CamelModel):
    id: int
    name: str
    parent_id: int | None
    OperationType: OperationTypeSchema


class CreateCategorySchema(CamelModel):
    name: str
    parent_id: int | None
    operation_type_id: int
