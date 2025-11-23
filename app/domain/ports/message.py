from typing import Protocol

from app.domain.models.message import MessageEntity


class MessageRepository(Protocol):
    def create(self, message: MessageEntity) -> MessageEntity: ...
    def get_dialog_history(
        self, dialog_id: int, limit: int = 10
    ) -> list[MessageEntity]: ...
    def delete_by_dialog_id(self, dialog_id: int) -> None: ...
