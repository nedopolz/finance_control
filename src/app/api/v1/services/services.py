from functools import lru_cache

from src.app.api.v1.models.models import User, Account, Status, Currency, AccountType
from src.app.db import database


class UserService:
    def __init__(self):
        self.database = database

    async def get_user_by_external_id(self, external_id: str):
        query = User.__table__.select().where(User.external_id == external_id)
        user = await self.database.fetch_one(query)
        return user


class AccountService:
    def __init__(self):
        self.database = database

    async def get_accounts_by_user_id(self, user_id: int):
        query = Account.__table__.select().join(Status).where(Account.user_id == user_id)
        accounts = await self.database.fetch_all(query)
        return accounts

    async def create_account(self, params: dict):
        status = await self.database.fetch_all(Status.__table__.select().where(Status.code == 'active'))
        query = Account.__table__.insert().values(status_id=status[0].id, **params)
        account = await self.database.execute(query)
        return account


@lru_cache()
def get_user_service():
    return UserService()


@lru_cache()
def get_account_service():
    return AccountService()
