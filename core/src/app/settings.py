from pydantic import BaseSettings, Field
import os
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    algorithm: str = Field(os.getenv("ALGORITHM"), env="ALGORITHM")
    database_host: str = Field(os.getenv("DATABASE_HOST"), env="DATABASE_HOST")
    database_port: int = Field(os.getenv("DATABASE_PORT"), env="DATABASE_PORT")
    database_user: str = Field(os.getenv("DATABASE_USER"), env="DATABASE_USER")
    database_password: str = Field(os.getenv("DATABASE_PASSWORD"), env="DATABASE_PASSWORD")
    database_name: str = Field(os.getenv("DATABASE_NAME"), env="DATABASE_NAME")
    kafka_host: str = Field(os.getenv("KAFKA_HOST"), env="KAFKA_HOST")
    kafka_topic: str = Field(os.getenv("KAFKA_TOPIC"), env="KAFKA_TOPIC")

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.database_user}:{self.database_password}@"
            f"{self.database_host}:{self.database_port}/{self.database_name}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
