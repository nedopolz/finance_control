from fastapi import APIRouter, Depends
from starlette import status

from src.app.api.v1.schemas.measurment import Measurement
from src.app.api.v1.services.services import (
    get_measurement_service,
    get_auth_service,
    get_device_service,
)
from src.app.security import get_current_user

router = APIRouter()


@router.post(
    "/",
    description="Отправить данные об измерении",
    responses={status.HTTP_200_OK: {"status": "ok"}},
)
async def measurement(
    data: Measurement,
    measurement_service=Depends(get_measurement_service),
    auth_service=Depends(get_auth_service),
    device_service=Depends(get_device_service),
    current_user=Depends(get_current_user),
):
    patient = await auth_service.get_patient(current_user.user_id)
    device = await device_service.get_by_patient_id(patient)
    return await measurement_service.add_measurement(
        data, patient_id=dict(patient).get("patient_id"), device_id=device
    )
