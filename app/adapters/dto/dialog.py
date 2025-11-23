from datetime import datetime

from pydantic import BaseModel, Field


class SaveMessageRequest(BaseModel):
    """Запрос на сохранение сообщения"""

    tg_id: int = Field(..., description="Telegram ID пользователя")
    role: str = Field(..., description="Роль: 'user' или 'assistant'")
    content: str = Field(..., description="Текст сообщения")

    class Config:
        json_schema_extra = {
            "example": {
                "tg_id": 123456789,
                "role": "user",
                "content": "Привет! Как дела?",
            }
        }


class SaveMessageResponse(BaseModel):
    """Ответ на сохранение сообщения"""

    id: int
    dialog_id: int
    role: str
    content: str
    created_at: datetime


class MessageDTO(BaseModel):
    """DTO для одного сообщения в истории"""

    role: str
    content: str


class GetHistoryResponse(BaseModel):
    """Ответ с историей диалога"""

    messages: list[MessageDTO]
    total: int = Field(..., description="Количество сообщений в истории")

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {"role": "user", "content": "Привет!"},
                    {"role": "assistant", "content": "Здравствуйте! Чем могу помочь?"},
                ],
                "total": 2,
            }
        }


class ResetDialogRequest(BaseModel):
    """Запрос на сброс диалога"""

    tg_id: int = Field(..., description="Telegram ID пользователя")


class ResetDialogResponse(BaseModel):
    """Ответ на сброс диалога"""

    success: bool
    message: str
