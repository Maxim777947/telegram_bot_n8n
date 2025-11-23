from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from app.domain.exceptions import UsernameAlreadyExistsError
from app.domain.ports.user import UserEntity, UserRepository


class CreateUserUseCase:
    def __init__(self, users: UserRepository):
        self.users = users

    def execute(
        self,
        tg_id: int,
        first_name: str,
        last_name: str,
        is_bot: bool,
        language_code: str,
        username: str,
    ) -> UserEntity:
        try:
            user = self.users.upsert(
                UserEntity(
                    tg_id=tg_id,
                    first_name=first_name,
                    last_name=last_name,
                    is_bot=is_bot,
                    language_code=language_code,
                    username=username,
                    created_at=datetime.now(timezone.utc),
                )
            )
            return self.users.get_by_id(user.id)
        except IntegrityError as e:
            if "users_username_key" in str(e.orig):
                raise UsernameAlreadyExistsError(username)
            raise
