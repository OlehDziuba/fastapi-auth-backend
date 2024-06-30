import jwt
import pydantic_settings

from auth_backend.app import UserTokenHandler, UserTokenPayload, InvalidTokenError


class JWTHandlerSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="JWT_", case_sensitive=False)
    secret_key: str


class JWTHandler(UserTokenHandler):
    def __init__(self, settings: JWTHandlerSettings):
        self._settings = settings

    def generate(self, payload: UserTokenPayload) -> str:
        return jwt.encode(payload.model_dump(mode="json"), self._settings.secret_key, algorithm="HS256")

    def decode(self, token: str) -> UserTokenPayload:
        try:
            return jwt.decode(token, self._settings.secret_key, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            raise InvalidTokenError
