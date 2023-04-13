from databases import Database

from src.app.api.v1.services.Kafkaservice import KafkaConsumer
from src.app.settings import settings
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(settings.database_url, echo=True)
Base = declarative_base()
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

database = Database(settings.database_url, min_size=5, max_size=20)
kafka = KafkaConsumer(topic=settings.kafka_topic, host=settings.kafka_host)
