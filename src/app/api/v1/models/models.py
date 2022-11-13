from sqlalchemy import Column, Integer, String, ForeignKey, MetaData
from sqlalchemy.orm import declarative_base, relationship

from src.app.db import database

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String, nullable=True)
    tg_id = Column(Integer, nullable=True)
    accounts = relationship("Account", back_populates="user")

    def __repr__(self):
        return f"tg_id:{self.tg_id}, external_id:{self.external_id}"


class Status(Base):
    __tablename__ = "statuses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    name = Column(String)
    accounts = relationship("Account", back_populates="status")


class AccountType(Base):
    __tablename__ = "account_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    name = Column(String)
    account = relationship("Account", back_populates="account_type")


class Currency(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    name = Column(String)
    symbol = Column(String)
    account = relationship("Account", back_populates="currency")


class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("statuses.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("account_types.id"), nullable=False)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=False)
    user = relationship("User", back_populates="accounts")
    currency = relationship("Currency", back_populates="account")
    account_type = relationship("AccountType", back_populates="account")
    status = relationship("Status", back_populates="accounts")
