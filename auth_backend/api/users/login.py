from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from auth_backend.app import AuthData, UserLoginInteractor


@inject
async def login(
        auth_data: AuthData,
        interactor: UserLoginInteractor = Depends(Provide["user_login_interactor"])
) -> str:
    token = await interactor(auth_data)

    return token
