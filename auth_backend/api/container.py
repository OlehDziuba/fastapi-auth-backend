from dependency_injector import containers, providers

from asyncpg import Pool

from auth_backend.adapters import BCryptPasswordHasher, BCryptPasswordHasherSettings, JWTHandler, JWTHandlerSettings
from auth_backend.app import UserRegistrateInteractor, UserLoginInteractor
from auth_backend.infrastructure.postgres import AsyncpgUsersRepository, DBSettings, create_pool


async def resource_pool(db_settings: DBSettings,) -> Pool:
    pool = await create_pool(db_settings)

    yield pool

    await pool.close()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["reservation_meeting_instructions_api.api"])

    db_settings = providers.Singleton(DBSettings)
    pool = providers.Resource(resource_pool, db_settings)

    users_repository = providers.Singleton(AsyncpgUsersRepository, pool)

    bcrypt_password_hasher_settings = providers.Singleton(BCryptPasswordHasherSettings)
    bcrypt_password_hasher = providers.Singleton(BCryptPasswordHasher, bcrypt_password_hasher_settings)

    jwt_token_handler_settings = providers.Singleton(JWTHandlerSettings)
    jwt_token_handler = providers.Singleton(JWTHandler, jwt_token_handler_settings)

    user_registrate_interactor = providers.Singleton(
        UserRegistrateInteractor,
        users_repository,
        bcrypt_password_hasher
    )

    user_login_interactor = providers.Singleton(
        UserLoginInteractor,
        users_repository,
        bcrypt_password_hasher,
        jwt_token_handler
    )
