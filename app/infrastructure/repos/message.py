from datetime import datetime, timezone

from sqlmodel import select

from app.domain.models.message import MessageEntity
from app.domain.ports.message import MessageRepository
from app.infrastructure.db.models.message import Message
from app.infrastructure.db.postgres import get_session


class MessageRepoSQL(MessageRepository):
    """SQL реализация репозитория сообщений"""

    def create(self, message: MessageEntity) -> MessageEntity:
        """Создать новое сообщение"""
        with get_session() as session:
            db_message = Message(
                dialog_id=message.dialog_id,
                role=message.role,
                content=message.content,
                created_at=message.created_at or datetime.now(timezone.utc),
            )
            session.add(db_message)
            session.commit()
            session.refresh(db_message)

            return MessageEntity(
                id=db_message.id,
                dialog_id=db_message.dialog_id,
                role=db_message.role,
                content=db_message.content,
                created_at=db_message.created_at,
            )

    def get_dialog_history(
        self, dialog_id: int, limit: int = 10
    ) -> list[MessageEntity]:
        """Получить последние N сообщений диалога (для контекста)"""
        with get_session() as session:
            statement = (
                select(Message)
                .where(Message.dialog_id == dialog_id)
                .order_by(Message.created_at.desc())
                .limit(limit)
            )

            db_messages = session.exec(statement).all()

            # Возвращаем в хронологическом порядке (старые -> новые)
            messages = [
                MessageEntity(
                    id=msg.id,
                    dialog_id=msg.dialog_id,
                    role=msg.role,
                    content=msg.content,
                    created_at=msg.created_at,
                )
                for msg in reversed(db_messages)
            ]

            return messages

    def delete_by_dialog_id(self, dialog_id: int) -> None:
        """Удалить все сообщения диалога"""
        with get_session() as session:
            statement = select(Message).where(Message.dialog_id == dialog_id)
            messages = session.exec(statement).all()

            for message in messages:
                session.delete(message)

            session.commit()
