from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Float, DateTime, Date
from sqlalchemy.orm import declarative_base, relationship


metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String, nullable=True)
    tg_id = Column(Integer, nullable=True)

    def __repr__(self):
        return f"tg_id:{self.tg_id}, external_id:{self.external_id}"
