import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
POSTGRES_USER = str(os.getenv("DATABASE_USER"))
POSTGRES_PASSWORD = str(os.getenv("DATABASE_PASSWORD"))
POSTGRES_DB = str(os.getenv("DATABASE_NAME"))
DBHOST = str(os.getenv("DATABASE_HOST"))
database_url = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DBHOST}/{POSTGRES_DB}"

admins = [
    419519710,
]

admin_chat_id = int(os.getenv("admin_chat_id"))
admin_channel_id = int(os.getenv("admin_channel_id"))

ip = os.getenv("ip")

aiogram_redis = {
    "host": ip,
}

debug = False

redis = {"address": (ip, 6379), "encoding": "utf8"}
