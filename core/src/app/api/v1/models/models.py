from sqlalchemy import Column, Integer, String, ForeignKey, MetaData, Float, DateTime, Date
from sqlalchemy.orm import declarative_base, relationship


metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    external_id = Column(String, nullable=True)
    tg_id = Column(Integer, nullable=True)
    accounts = relationship("Account", back_populates="user")
    categories = relationship("Category", back_populates="user")

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
    operations = relationship("Operation", back_populates="account")


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    operation_type_id = Column(Integer, ForeignKey("operation_types.id"), nullable=False)
    operation_type = relationship("OperationType", back_populates="categories")
    user = relationship("User", back_populates="categories")
    children = relationship("Category", back_populates="parent")
    parent = relationship("Category", remote_side=[id], back_populates="children")
    operations = relationship("Operation", back_populates="category")


class OperationType(Base):
    __tablename__ = "operation_types"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String)
    name = Column(String)
    categories = relationship("Category", back_populates="operation_type")
    operations = relationship("Operation", back_populates="operation_type")


class Operation(Base):
    __tablename__ = "operations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    type_id = Column(Integer, ForeignKey("operation_types.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    account = relationship("Account", back_populates="operations")
    category = relationship("Category", back_populates="operations")
    operation_type = relationship("OperationType", back_populates="operations")
