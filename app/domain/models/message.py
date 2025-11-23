from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class MessageEntity:
    dialog_id: int
    role: str
    content: str
    created_at: datetime
    id: Optional[int] = None
