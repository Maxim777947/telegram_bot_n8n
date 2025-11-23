from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class DialogEntity:
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    id: Optional[int] = None
