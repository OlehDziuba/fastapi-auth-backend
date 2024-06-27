import bcrypt
import pydantic_settings

from auth_backend.app import PasswordHasher


class BCryptPasswordHasherSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="BCRYPT_", case_sensitive=False)

    salt: str


class BCryptPasswordHasher(PasswordHasher):
    def __init__(self, settings: BCryptPasswordHasherSettings):
        self._settings = settings

    def hash(self, raw_password: str) -> str:
        return bcrypt.hashpw(raw_password.encode(), self._settings.salt.encode()).decode()
