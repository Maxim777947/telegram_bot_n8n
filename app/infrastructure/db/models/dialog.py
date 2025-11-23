from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class Dialog(SQLModel, table=True):
    """Модель диалога (сессия разговора)"""

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    is_active: bool = Field(default=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: list["Message"] = Relationship(back_populates="dialog")

    __tablename__ = "dialogs"
