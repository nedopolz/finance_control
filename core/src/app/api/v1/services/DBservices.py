from functools import lru_cache
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.v1.models.models import User, Account, Status, Currency, AccountType, Category, OperationType, \
    Operation
from src.app.api.v1.schemas.account import AccountSchema
from src.app.api.v1.schemas.сategory import CategorySchema


class UserService:
    def __init__(self):
        from src.app.loaders import database
        self.database = database

    async def get_user_by_external_id(self, external_id: str):
        query = User.__table__.select().where(User.external_id == external_id)
        user = await self.database.fetch_one(query)
        return user

    async def create_user(self, external_id):
        query = User.__table__.insert().values(external_id=external_id)
        user = await self.database.execute(query)
        return user


class AccountService:
    def __init__(self):
        from src.app.loaders import database
        self.database = database

    async def get_accounts_by_user_id(self, user_id: int, session: AsyncSession) -> List[AccountSchema]:
        accounts = await session.execute(
            select(Account, Status, AccountType, Currency).join(Status).join(AccountType).join(Currency).where(
                Account.user_id == user_id)
        )
        accounts = [dict(account) for account in accounts]
        return [AccountSchema(id=account["Account"].id, **account) for account in accounts]

    async def create_account(self, params: dict):
        status = await self.database.fetch_all(Status.__table__.select().where(Status.code == "active"))
        query = Account.__table__.insert().values(status_id=status[0].id, **params)
        account = await self.database.execute(query)
        return account

    async def delete_account(self, account_id, user_id):
        query = Account.__table__.delete().where(Account.id == account_id).where(Account.user_id == user_id)
        account = await self.database.execute(query)
        return account

    async def validate_account_id(self, account_id, user_id):
        query = Account.__table__.select().where(Account.id == account_id, Account.user_id == user_id)
        account = await self.database.fetch_one(query)
        return account


class CategoryService:
    def __init__(self):
        from src.app.loaders import database
        self.database = database

    async def get_category_by_user_id(self, user_id: int, session: AsyncSession) -> List[CategorySchema]:
        categories = await session.execute(
            select(Category, OperationType).join(OperationType).where(Category.user_id == user_id)
        )
        categories = [dict(category) for category in categories]
        return [CategorySchema(id=c["Category"].id, name=c["Category"].name, parent_id=c["Category"].parent_id, **c) for
                c in categories]

    async def create_category(self, params: dict):
        query = Category.__table__.insert().values(**params)
        category = await self.database.execute(query)
        return category

    async def validate_category_id(self, category_id):
        query = Category.__table__.select().where(Category.id == category_id)
        category = await self.database.fetch_one(query)
        return category

    async def delete_category(self, category_id, user_id):
        query = Category.__table__.delete().where(Category.id == category_id).where(Category.user_id == user_id)
        category = await self.database.execute(query)
        return category


class OperationService:
    def __init__(self):
        from src.app.loaders import database
        self.database = database

    async def create_operation(self, params: dict):
        query = Operation.__table__.insert().values(**params)
        operation = await self.database.execute(query)
        return operation


@lru_cache()
def get_userDB_service():
    return UserService()


@lru_cache()
def get_accountDB_service():
    return AccountService()


@lru_cache()
def get_categoryDB_service():
    return CategoryService()


@lru_cache()
def get_operationDB_service():
    return OperationService()
