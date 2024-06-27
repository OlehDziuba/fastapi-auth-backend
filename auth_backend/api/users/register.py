from dependency_injector.wiring import Provide, inject
from fastapi import Depends

from auth_backend.app import UserRegistrationInput, UserRegistrateInteractor
from .common import UserResponse


@inject
async def register_user(
        registration_input: UserRegistrationInput,
        interactor: UserRegistrateInteractor = Depends(Provide["user_registrate_interactor"])
) -> UserResponse:
    user = await interactor(registration_input)

    return UserResponse.from_user(user)
