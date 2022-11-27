from functools import lru_cache
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.v1.models.models import User, Account, Status, Currency, AccountType
from src.app.api.v1.schemas.account import AccountSchema
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

    async def validate_account_id(self, account_id):
        query = Account.__table__.select().where(Account.id == account_id)
        account = await self.database.fetch_one(query)
        return account


@lru_cache()
def get_userDB_service():
    return UserService()


@lru_cache()
def get_accountDB_service():
    return AccountService()
