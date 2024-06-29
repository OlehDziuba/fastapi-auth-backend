from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from auth_backend.app import AuthData, UserLoginInteractor, UserEmailDoesNotExistError, PasswordDoesNotMatchError


@inject
async def login(
        auth_data: AuthData,
        interactor: UserLoginInteractor = Depends(Provide["user_login_interactor"])
) -> str:
    try:
        token = await interactor(auth_data)
    except (UserEmailDoesNotExistError, PasswordDoesNotMatchError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return token
