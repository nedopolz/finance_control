from databases import Database
from src.app.settings import settings



database = Database(settings.database_url, min_size=5, max_size=20)
