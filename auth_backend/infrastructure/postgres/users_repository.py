from uuid import UUID

from asyncpg import Pool

from auth_backend.app import UsersRepository
from auth_backend.core import User


class AsyncpgUsersRepository(UsersRepository):
    def __init__(self, pool: Pool):
        self._pool = pool

    async def get_by_id(self, user_id: UUID) -> User | None:
        user_record = await self._pool.fetchrow(
            f"""
                SELECT id, email, password, first_name, last_name, created_at, updated_at, last_login_at
                FROM users
                WHERE id = $1::UUID
            """, user_id
        )

        return User.model_validate(dict(user_record)) if user_record else None

    async def get_by_email(self, email: str) -> User | None:
        user_record = await self._pool.fetchrow(
            f"""
                SELECT id, email, password, first_name, last_name, created_at, updated_at, last_login_at
                FROM users
                WHERE email = $1::TEXT
            """, email
        )

        return User.model_validate(dict(user_record)) if user_record else None

    async def create(self, user: User) -> None:
        await self._pool.execute(
            f"""
                INSERT INTO users (id, email, password, first_name, last_name, created_at, updated_at, last_login_at)
                VALUES ($1::UUID, $2::TEXT, $3::TEXT, $4::TEXT, $5::TEXT, $6::TIMESTAMP, $7::TIMESTAMP, $8::TIMESTAMP)
            """,
            user.id, user.email, user.password, user.first_name, user.last_name, user.created_at,
            user.updated_at, user.last_login_at
        )

    async def update(self, user: User) -> None:
        await self._pool.execute(
            f"""
                UPDATE users 
                SET
                    email = $2::TEXT,
                    password = $3::TEXT,
                    first_name = $4::TEXT,
                    last_name = $5::TEXT,
                    updated_at = $6::TIMESTAMP,
                    last_login_at = $7::TIMESTAMP
                WHERE id = $1::UUID
            """,
            user.id, user.email, user.password, user.first_name, user.last_name, user.updated_at, user.last_login_at
        )
