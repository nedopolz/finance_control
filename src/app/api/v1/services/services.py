from datetime import datetime
from functools import lru_cache

from src.app.api.v1.services.DBservices import get_accountDB_service, get_categoryDB_service, get_operationDB_service


class AccountService:
    def __init__(self):
        self.db_service = get_accountDB_service()

    async def delete_account(self, account_id, user_id):
        account = await self.db_service.validate_account_id(account_id)
        if account:
            await self.db_service.delete_account(account_id, user_id)
            return True
        return False


class CategoryService:
    def __init__(self):
        self.db_service = get_categoryDB_service()

    async def create_category(self, params: dict):
        category = await self.db_service.create_category(params)
        return category

    async def delete_category(self, category_id, user_id):
        category = await self.db_service.validate_category_id(category_id)
        if category:
            await self.db_service.delete_category(category_id, user_id)
            return True
        return False

    async def validate_category_id(self, category_id):
        category = await self.db_service.validate_category_id(category_id)
        return category


class OperationService:
    def __init__(self):
        self.db_service = get_operationDB_service()
        self.account_service = get_accountDB_service()
        self.category_service = get_categoryDB_service()

    async def create_operation(self, params: dict, user_id):
        account = await self.account_service.validate_account_id(params["account_id"], user_id)
        if not account:
            return False
        category = await self.category_service.validate_category_id(params["category_id"])
        if not category:
            return False

        if not params.get("datetime"):
            params["datetime"] = datetime.now()
        else:
            params["datetime"] = datetime.strptime(params["datetime"], "%d.%m.%Y %H:%M")
        operation = await self.db_service.create_operation(params)
        return operation


@lru_cache()
def get_account_service():
    return AccountService()

@lru_cache()
def get_category_service():
    return CategoryService()

@lru_cache()
def get_operation_service():
    return OperationService()
