from datetime import datetime

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    tg_id: int
    first_name: str
    last_name: str
    is_bot: bool
    language_code: str
    username: str


class CreateUserResponse(BaseModel):
    id: int
    tg_id: int
    username: str
    first_name: str
    last_name: str
    is_bot: bool
    language_code: str
    created_at: datetime
