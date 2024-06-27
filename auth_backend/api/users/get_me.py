from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Header

from auth_backend.app import GetUserByTokenInteractor
from .common import UserResponse


@inject
async def get_me(
        authorization: Annotated[str, Header()],
        interactor: GetUserByTokenInteractor = Depends(Provide["get_user_by_token_interactor"])
) -> UserResponse:
    user = await interactor(authorization)

    return UserResponse.from_user(user)
