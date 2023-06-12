from fastapi import Depends, HTTPException, status

from app.auth.adapters.jwt_service import JWTData
from app.auth.service import Service, get_service
from app.auth.router.dependencies import parse_jwt_user_data
from . import router
from app.auth.repository.repository import AuthRepository
from app.utils import AppModel


class GetMyAccountResponse(AppModel):
    _id: str
    email: str
    phone: str
    name: str
    city: str


@router.get("/users/me", response_model=GetMyAccountResponse)
def get_my_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    repository: AuthRepository = svc.repository

    user = repository.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return GetMyAccountResponse(**user)
