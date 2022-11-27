from src.app.api.v1.models.models import Status, AccountType, Currency, OperationType
from src.app.api.v1.services.defaults_db_values import account_status, account_type, currency, operation_type


class DBStartUp:
    def __init__(self, db):
        self.db = db

    async def check_table_for_defaults(self, table, defaults):
        for default in defaults:
            query = table.__table__.select().where(table.code == default["code"])
            result = await self.db.fetch_one(query)
            if not result:
                query = table.__table__.insert().values(**default)
                await self.db.execute(query)

    async def init_table_defaults(self):
        await self.check_table_for_defaults(Status, account_status)
        await self.check_table_for_defaults(AccountType, account_type)
        await self.check_table_for_defaults(Currency, currency)
        await self.check_table_for_defaults(OperationType, operation_type)
