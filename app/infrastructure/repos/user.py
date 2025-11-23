from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.exc import IntegrityError
from sqlmodel import select

from app.domain.ports.user import UserEntity, UserRepository
from app.infrastructure.db.models.user import UserMetadata
from app.infrastructure.db.postgres import get_session


class UserRepoSQL(UserRepository):
    def upsert(self, user: UserEntity) -> UserEntity:
        with get_session() as session:
            db_user = session.exec(
                select(UserMetadata).where(UserMetadata.tg_id == user.tg_id)
            ).first()

            if db_user:
                db_user.first_name = user.first_name
                db_user.last_name = user.last_name
                db_user.is_bot = user.is_bot
                db_user.language_code = user.language_code
                db_user.username = user.username
            else:
                db_user = UserMetadata(
                    tg_id=user.tg_id,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    is_bot=user.is_bot,
                    language_code=user.language_code,
                    username=user.username,
                    created_at=user.created_at or datetime.now(timezone.utc),
                )
                session.add(db_user)

            try:
                session.commit()
            except IntegrityError as e:
                session.rollback()
                raise
            session.refresh(db_user)
            return UserEntity(
                id=db_user.id,
                tg_id=db_user.tg_id,
                first_name=db_user.first_name or "",
                last_name=db_user.last_name or "",
                is_bot=db_user.is_bot or False,
                language_code=db_user.language_code or "",
                username=db_user.username,
                created_at=db_user.created_at,
            )

    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        with get_session() as session:
            db_user = session.get(UserMetadata, user_id)
            if not db_user:
                return None
            return UserEntity(
                id=db_user.id,
                tg_id=db_user.tg_id,
                first_name=db_user.first_name or "",
                last_name=db_user.last_name or "",
                is_bot=db_user.is_bot or False,
                language_code=db_user.language_code or "",
                username=db_user.username,
                created_at=db_user.created_at,
            )

    def get_by_tg_id(self, tg_id: int) -> Optional[UserEntity]:
        with get_session() as session:
            db_user = session.exec(
                select(UserMetadata).where(UserMetadata.tg_id == tg_id)
            ).first()
            if not db_user:
                return None
            return UserEntity(
                id=db_user.id,
                tg_id=db_user.tg_id,
                first_name=db_user.first_name or "",
                last_name=db_user.last_name or "",
                is_bot=db_user.is_bot or False,
                language_code=db_user.language_code or "",
                username=db_user.username,
                created_at=db_user.created_at,
            )
