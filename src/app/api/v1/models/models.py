from sqlalchemy import (
    Column,
    INTEGER,
    FLOAT,
    String,
    DateTime,
    ForeignKey,
    Table,
    MetaData,
)


metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("user_id", INTEGER, primary_key=True, nullable=False),
    Column("first_name", String, nullable=False, index=True),
    Column("last_name", String, nullable=False),
    Column("patronymic", String, nullable=False),
    Column("email", String, nullable=False, index=True, unique=True),
    Column("password", String, nullable=False),
)

patients = Table(
    "patients",
    metadata,
    Column("patient_id", INTEGER, primary_key=True, index=True),
    Column("doctor_id", INTEGER, nullable=False, index=True),
    Column("users_id", INTEGER, ForeignKey("users.user_id"), nullable=False),
)

devices = Table(
    "devices",
    metadata,
    Column("device_id", INTEGER, primary_key=True, index=True, nullable=False),
    Column("patient_id", INTEGER, ForeignKey("patients.patient_id")),
    Column("uid", INTEGER, index=True, nullable=False, unique=True),
    Column("charge", INTEGER, nullable=False),
)

doctors = Table(
    "doctors",
    metadata,
    Column("doctor_id", INTEGER, primary_key=True, nullable=False),
    Column("user_id", INTEGER, ForeignKey("users.user_id")),
)

measurements = Table(
    "measurements",
    metadata,
    Column("measurement_id", INTEGER, primary_key=True, nullable=False),
    Column("patient_id", INTEGER, ForeignKey("patients.patient_id")),
    Column("device_id", INTEGER, ForeignKey("devices.device_id"), nullable=False),
    Column("measurement_value", FLOAT, nullable=False),
    Column("time", DateTime, nullable=False),
)
