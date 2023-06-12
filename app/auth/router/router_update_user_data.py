from fastapi import Depends, HTTPException, status

from app.auth.adapters.jwt_service import JWTData
from app.auth.service import Service, get_service
from app.auth.router.dependencies import parse_jwt_user_data
from . import router
from app.auth.repository.repository import AuthRepository
from app.utils import AppModel


class UpdateUserDataRequest(AppModel):
    phone: str
    name: str
    city: str


@router.patch("/users/me", status_code=status.HTTP_200_OK)
def update_user_data(
    data: UpdateUserDataRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    repository: AuthRepository = svc.repository

    try:
        repository.update_user_data(user_id, data.dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return {"message": "User data updated successfully"}
