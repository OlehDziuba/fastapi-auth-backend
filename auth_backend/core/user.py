import pydantic

from datetime import datetime
from uuid import UUID, uuid4


class User(pydantic.BaseModel):
    id: UUID = pydantic.Field(default_factory=uuid4)
    email: pydantic.EmailStr
    password: str
    first_name: str
    last_name: str
    created_at: datetime = pydantic.Field(default_factory=datetime.utcnow)
    updated_at: datetime = pydantic.Field(default_factory=datetime.utcnow)
    last_login_at: datetime = pydantic.Field(default_factory=datetime.utcnow)
