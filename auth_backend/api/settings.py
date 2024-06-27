import pydantic_settings


class ServerSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="SERVER_", case_sensitive=False)

    address: str


