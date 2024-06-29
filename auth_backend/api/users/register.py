from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status

from auth_backend.app import EmailAlreadyExistsError, UserRegistrationInput, UserRegistrateInteractor
from .common import UserResponse


@inject
async def register_user(
        registration_input: UserRegistrationInput,
        interactor: UserRegistrateInteractor = Depends(Provide["user_registrate_interactor"])
) -> UserResponse:
    try:
        user = await interactor(registration_input)
    except EmailAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')

    return UserResponse.from_user(user)
