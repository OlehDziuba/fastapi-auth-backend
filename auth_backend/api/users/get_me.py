from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Header, HTTPException, status

from auth_backend.app import GetUserByTokenInteractor, InvalidTokenError, UserEmailDoesNotExistError
from .common import UserResponse


@inject
async def get_me(
        authorization: Annotated[str, Header()],
        interactor: GetUserByTokenInteractor = Depends(Provide["get_user_by_token_interactor"])
) -> UserResponse:
    try:
        user = await interactor(authorization)
    except (InvalidTokenError, UserEmailDoesNotExistError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    return UserResponse.from_user(user)
