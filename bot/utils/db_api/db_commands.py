import logging

from utils.db_api.db import database
from utils.db_api.models.models import User


class UserDB:
    def __init__(self):
        self.database = database

    async def get_user_by_tg_id(self, tg_id):
        query = User.__table__.select().where(User.tg_id == tg_id)
        user = await self.database.fetch_one(query)
        return user
