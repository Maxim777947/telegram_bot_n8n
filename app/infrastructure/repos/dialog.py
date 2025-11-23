from datetime import datetime, timezone
from typing import Optional

from sqlmodel import select

from app.domain.models.dialog import DialogEntity
from app.domain.ports.dialog import DialogRepository
from app.infrastructure.db.models.dialog import Dialog
from app.infrastructure.db.postgres import get_session


class DialogRepoSQL(DialogRepository):
    """SQL реализация репозитория диалогов"""

    def create(self, dialog: DialogEntity) -> DialogEntity:
        """Создать новый диалог"""
        with get_session() as session:
            db_dialog = Dialog(
                user_id=dialog.user_id,
                is_active=dialog.is_active,
                created_at=dialog.created_at or datetime.now(timezone.utc),
                updated_at=dialog.updated_at or datetime.now(timezone.utc),
            )
            session.add(db_dialog)
            session.commit()
            session.refresh(db_dialog)

            return DialogEntity(
                id=db_dialog.id,
                user_id=db_dialog.user_id,
                is_active=db_dialog.is_active,
                created_at=db_dialog.created_at,
                updated_at=db_dialog.updated_at,
            )

    def get_by_id(self, dialog_id: int) -> Optional[DialogEntity]:
        """Получить диалог по ID"""
        with get_session() as session:
            db_dialog = session.get(Dialog, dialog_id)
            if not db_dialog:
                return None

            return DialogEntity(
                id=db_dialog.id,
                user_id=db_dialog.user_id,
                is_active=db_dialog.is_active,
                created_at=db_dialog.created_at,
                updated_at=db_dialog.updated_at,
            )

    def get_active_by_user_id(self, user_id: int) -> Optional[DialogEntity]:
        """Получить активный диалог пользователя"""
        with get_session() as session:
            statement = (
                select(Dialog)
                .where(Dialog.user_id == user_id, Dialog.is_active == True)
                .order_by(Dialog.updated_at.desc())
            )

            db_dialog = session.exec(statement).first()
            if not db_dialog:
                return None

            return DialogEntity(
                id=db_dialog.id,
                user_id=db_dialog.user_id,
                is_active=db_dialog.is_active,
                created_at=db_dialog.created_at,
                updated_at=db_dialog.updated_at,
            )

    def update(self, dialog: DialogEntity) -> DialogEntity:
        """Обновить диалог"""
        with get_session() as session:
            db_dialog = session.get(Dialog, dialog.id)
            if not db_dialog:
                raise ValueError(f"Dialog with id {dialog.id} not found")

            db_dialog.is_active = dialog.is_active
            db_dialog.updated_at = datetime.now(timezone.utc)

            session.add(db_dialog)
            session.commit()
            session.refresh(db_dialog)

            return DialogEntity(
                id=db_dialog.id,
                user_id=db_dialog.user_id,
                is_active=db_dialog.is_active,
                created_at=db_dialog.created_at,
                updated_at=db_dialog.updated_at,
            )

    def deactivate_user_dialogs(self, user_id: int) -> None:
        """Деактивировать все диалоги пользователя"""
        with get_session() as session:
            statement = select(Dialog).where(
                Dialog.user_id == user_id, Dialog.is_active == True
            )
            dialogs = session.exec(statement).all()

            for dialog in dialogs:
                dialog.is_active = False
                dialog.updated_at = datetime.now(timezone.utc)
                session.add(dialog)

            session.commit()
