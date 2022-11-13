from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from starlette import status

from src.app.api.v1.dependencies import get_current_user
from src.app.api.v1.schemas.account import CreateAccount, Account
from src.app.api.v1.services.services import get_account_service

router = APIRouter()


@router.get(
    "/",
    description="Получить список счетов пользователя",
    response_model=List[Account]
)
async def get_accounts(
    current_user=Depends(get_current_user),
    account_service=Depends(get_account_service),
):
    accounts = await account_service.get_accounts_by_user_id(current_user.id)
    return accounts


@router.post(
    "/",
    description="Создать счет",
    responses={status.HTTP_200_OK: {"status": "ok"}},
)
async def create_account(
    account: CreateAccount,
    current_user=Depends(get_current_user),
    account_service=Depends(get_account_service),
):
    data = account.dict()
    data["user_id"] = current_user.id
    id = await account_service.create_account(data)
    return JSONResponse({"account_id": id})

