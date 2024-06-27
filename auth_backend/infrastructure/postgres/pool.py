import pydantic
import pydantic_settings

from typing import Self
from urllib.parse import quote

from asyncpg import create_pool as create_asyncpg_pool, Pool


class DBSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(env_prefix="POSTGRES_", case_sensitive=False)

    dbname: str
    user: str
    password: str
    address: str

    @pydantic.model_validator(mode="after")
    def _quote_variables(self) -> Self:
        self.dbname = quote(self.dbname, safe='')
        self.user = quote(self.user, safe='')
        self.password = quote(self.password, safe='')

        return self

    @property
    def dsn(self) -> str:
        dsn = f"postgresql://{self.user}:{self.password}@{self.address}/{self.dbname}"

        return dsn


async def create_pool(settings: DBSettings) -> Pool:
    pool = await create_asyncpg_pool(dsn=settings.dsn)

    return pool
