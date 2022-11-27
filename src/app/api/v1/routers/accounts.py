from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.api.v1.dependencies import get_current_user, get_session
from src.app.api.v1.schemas.account import CreateAccount, AccountSchema
from src.app.api.v1.services.DBservices import get_accountDB_service
from src.app.api.v1.services.services import get_account_service

router = APIRouter()


@router.get("/", description="Получить список счетов пользователя", response_model=List[AccountSchema])
async def get_accounts(
    current_user=Depends(get_current_user), account_service=Depends(get_accountDB_service), session: AsyncSession = Depends(get_session)
):
    accounts = await account_service.get_accounts_by_user_id(current_user.id, session)
    return accounts


@router.post(
    "/",
    description="Создать счет",
    responses={status.HTTP_200_OK: {"status": "ok"}},
)
async def create_account(
    account: CreateAccount,
    current_user=Depends(get_current_user),
    account_service=Depends(get_accountDB_service),
):
    data = account.dict()
    data["user_id"] = current_user.id
    id = await account_service.create_account(data)
    return JSONResponse({"account_id": id})


@router.delete(
    "/{account_id}",
    description="Удалить счет",
    responses={status.HTTP_200_OK: {"status": "ok"}, status.HTTP_404_NOT_FOUND: {"status": "not found"}},
)
async def delete_account(
    account_id: int,
    current_user=Depends(get_current_user),
    account_service=Depends(get_account_service),
):
    account = await account_service.delete_account(account_id, current_user.id)
    if account:
        return JSONResponse({"status": "ok"})
    return JSONResponse({"status": "not found"}, status_code=status.HTTP_404_NOT_FOUND)
