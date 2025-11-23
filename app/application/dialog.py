from datetime import datetime, timezone

from app.domain.models.dialog import DialogEntity
from app.domain.models.message import MessageEntity
from app.domain.ports.dialog import DialogRepository
from app.domain.ports.message import MessageRepository
from app.domain.ports.user import UserRepository


class SaveMessageUseCase:
    """Use Case для сохранения сообщения в диалог"""

    def __init__(
        self,
        users: UserRepository,
        dialogs: DialogRepository,
        messages: MessageRepository,
    ):
        self.users = users
        self.dialogs = dialogs
        self.messages = messages

    def execute(self, tg_id: int, role: str, content: str) -> MessageEntity:
        """
        Сохранить сообщение в активный диалог пользователя.
        Если активного диалога нет - создать новый.

        Args:
            tg_id: Telegram ID пользователя
            role: Роль отправителя ("user" или "assistant")
            content: Текст сообщения

        Returns:
            MessageEntity: Сохраненное сообщение
        """
        # Получаем пользователя
        user = self.users.get_by_tg_id(tg_id)
        if not user:
            raise ValueError(f"User with tg_id {tg_id} not found")

        # Получаем или создаем активный диалог
        dialog = self.dialogs.get_active_by_user_id(user.id)
        if not dialog:
            # Создаем новый диалог
            now = datetime.now(timezone.utc)
            dialog = self.dialogs.create(
                DialogEntity(
                    user_id=user.id,
                    is_active=True,
                    created_at=now,
                    updated_at=now,
                )
            )

        # Сохраняем сообщение
        message = self.messages.create(
            MessageEntity(
                dialog_id=dialog.id,
                role=role,
                content=content,
                created_at=datetime.now(timezone.utc),
            )
        )

        # Обновляем время последнего обновления диалога
        updated_dialog = DialogEntity(
            id=dialog.id,
            user_id=dialog.user_id,
            is_active=dialog.is_active,
            created_at=dialog.created_at,
            updated_at=datetime.now(timezone.utc),
        )
        self.dialogs.update(updated_dialog)

        return message


class GetDialogHistoryUseCase:
    """Use Case для получения истории диалога"""

    def __init__(
        self,
        users: UserRepository,
        dialogs: DialogRepository,
        messages: MessageRepository,
    ):
        self.users = users
        self.dialogs = dialogs
        self.messages = messages

    def execute(self, tg_id: int, limit: int = 10) -> list[MessageEntity]:
        """
        Получить последние N сообщений из активного диалога пользователя.

        Args:
            tg_id: Telegram ID пользователя
            limit: Количество последних сообщений (по умолчанию 10)

        Returns:
            list[MessageEntity]: Список сообщений (от старых к новым)
        """
        # Получаем пользователя
        user = self.users.get_by_tg_id(tg_id)
        if not user:
            return []

        # Получаем активный диалог
        dialog = self.dialogs.get_active_by_user_id(user.id)
        if not dialog:
            return []

        # Получаем историю сообщений
        return self.messages.get_dialog_history(dialog.id, limit)


class ResetDialogUseCase:
    """Use Case для сброса контекста диалога"""

    def __init__(
        self,
        users: UserRepository,
        dialogs: DialogRepository,
    ):
        self.users = users
        self.dialogs = dialogs

    def execute(self, tg_id: int) -> None:
        """
        Сбросить контекст диалога (деактивировать текущий диалог).
        При следующем сообщении будет создан новый диалог.

        Args:
            tg_id: Telegram ID пользователя
        """
        # Получаем пользователя
        user = self.users.get_by_tg_id(tg_id)
        if not user:
            raise ValueError(f"User with tg_id {tg_id} not found")

        # Деактивируем все диалоги пользователя
        self.dialogs.deactivate_user_dialogs(user.id)
