import datetime
import random
from functools import lru_cache

from passlib.context import CryptContext

from src.app.api.v1.models.models import users, measurements, patients, devices, doctors
from src.app.api.v1.schemas.measurment import Measurement
from src.app.api.v1.schemas.user import UserCreate, UserOptional, UserOut
from src.app.db import database


# TODO decompose this class to many
class AuthService:
    def __init__(self):
        self.database = database
        self.pw_manager = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    async def get_users(self, page: dict):
        users_query = users.select().offset(page["skip"]).limit(page["limit"])
        users_records = await self.database.fetch_all(users_query)
        return [UserOut(**user) for user in users_records]

    async def get_by_id(self, user_id: int):
        users_query = users.select().where(users.c.user_id == user_id)
        return await self.database.fetch_one(users_query)

    async def get_patient(self, user_id: int):
        users_query = patients.select().where(users.c.user_id == user_id)
        return await self.database.fetch_one(users_query)

    @database.transaction()
    async def signup_user(self, data: UserCreate):
        hashed_pw = self.hash_password(data.password)
        query = users.insert().values(
            first_name=data.first_name,
            last_name=data.last_name,
            patronymic=data.patronymic,
            email=data.email,
            password=hashed_pw,
        )
        user_id = await self.database.execute(query)  # id нового пользователя
        user = data.dict()
        del user["password"]
        query = doctors.insert().values(user_id=user_id)
        patient_id = await self.database.execute(query)
        return UserOut(user_id=user_id, **user)

    @database.transaction()
    async def create_user_patient_map(self, doctor_id: int, patient_id: int):
        query = patients.insert().values(doctor_id=doctor_id, users_id=patient_id)
        await self.database.execute(query)

    async def get_patients(self, user_id: int, page: dict):
        all_patients = (
            patients.select()
            .join(users, patients.c.users_id == users.c.user_id)
            .where(patients.c.doctor_id == user_id)
            .offset(page["skip"])
            .limit(page["limit"])
        )
        patients_records = await database.fetch_all(all_patients)
        return patients_records

    async def change_credentials(self, user_id: int, data: UserOptional):
        new_user_data = data.dict(exclude_unset=True)
        if "password" in new_user_data.keys():
            new_user_data["password"] = self.hash_password(data.password)
        query = users.update().where(users.c.user_id == user_id).values(**new_user_data)
        await self.database.execute(query)

    def serialized(self, user_records):
        all_users = []
        if isinstance(user_records, list):
            for u in user_records:
                all_users.append({k: v for k, v in dict(u).items() if k != "password"})
            return all_users
        return {k: v for k, v in dict(user_records).items() if k != "password"}

    async def delete_user(self, user_id: int):
        query = users.delete().where(users.c.user_id == user_id)
        return await self.database.execute(query)

    async def find_by_email(self, email: str):
        exists_query = users.select().where(users.c.email == email)
        return await self.database.fetch_one(exists_query)

    def verify_password(self, plain_password, hashed_password):
        return self.pw_manager.verify(plain_password, hashed_password)

    def hash_password(self, password: str):
        return self.pw_manager.hash(password)


class MeasurementService:
    def __init__(self):
        self.database = database
        self.pw_manager = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    async def add_measurement(self, data: Measurement, patient_id, device_id: int):
        query = measurements.insert().values(
            measurement_value=data.measurement_value,
            time=datetime.datetime.now(),
            patient_id=patient_id,
            device_id=device_id,
        )
        measurement_id = await self.database.execute(query)
        return measurement_id


class DeviceService:
    def __init__(self):
        self.database = database
        self.pw_manager = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    async def get_by_patient_id(self, patient_id: int):
        query = devices.select().where(devices.c.patient_id == patient_id)
        device_id = await self.database.execute(query)
        return device_id

    async def add_user(self, users_id, device_uid: int):
        if device_uid < 0:
            return None
        query = patients.select().where(
            patients.c.users_id == dict(users_id).get("user_id")
        )
        patient_id = await self.database.execute(query)
        query = devices.select().where(devices.c.patient_id == patient_id)
        device_id = await self.database.execute(query)
        if device_id:
            return None
        query = devices.insert().values(
            patient_id=patient_id, uid=device_uid, charge=100
        )
        device_id = await self.database.execute(query)
        return device_id


@lru_cache()
def get_auth_service():
    return AuthService()


@lru_cache()
def get_device_service():
    return DeviceService()


@lru_cache()
def get_measurement_service():
    return MeasurementService()
