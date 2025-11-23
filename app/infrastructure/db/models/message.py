from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class Message(SQLModel, table=True):
    """Модель сообщения в диалоге"""

    id: int | None = Field(default=None, primary_key=True)
    dialog_id: int = Field(foreign_key="dialogs.id", index=True)
    role: str = Field(index=True)  # "user" или "assistant"
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Связь с диалогом
    dialog: "Dialog" = Relationship(back_populates="messages")

    __tablename__ = "messages"
