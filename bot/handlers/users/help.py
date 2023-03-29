from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit
from utils.db_api.db_commands import UserDB


@rate_limit(5, "help")
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ["Список команд: ", "/start - Начать диалог", "/help - Получить справку"]
    await message.answer("\n".join(text))
