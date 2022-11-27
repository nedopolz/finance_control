from functools import lru_cache

from src.app.api.v1.services.DBservices import get_accountDB_service


class AccountService:
    def __init__(self):
        self.db_service = get_accountDB_service()

    async def delete_account(self, account_id, user_id):
        account = await self.db_service.validate_account_id(account_id)
        if account:
            await self.db_service.delete_account(account_id, user_id)
            return True
        return False


@lru_cache()
def get_account_service():
    return AccountService()
