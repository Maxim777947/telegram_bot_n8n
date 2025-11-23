from functools import lru_cache

from fastapi import Depends, HTTPException

from app.adapters.dto.dialog import (
    GetHistoryResponse,
    MessageDTO,
    ResetDialogRequest,
    ResetDialogResponse,
    SaveMessageRequest,
    SaveMessageResponse,
)
from app.application.dialog import (
    GetDialogHistoryUseCase,
    ResetDialogUseCase,
    SaveMessageUseCase,
)
from app.infrastructure.repos.dialog import DialogRepoSQL
from app.infrastructure.repos.message import MessageRepoSQL
from app.infrastructure.repos.user import UserRepoSQL

from .common import router


@lru_cache
def get_save_message_usecase() -> SaveMessageUseCase:
    return SaveMessageUseCase(
        users=UserRepoSQL(),
        dialogs=DialogRepoSQL(),
        messages=MessageRepoSQL(),
    )


@lru_cache
def get_dialog_history_usecase() -> GetDialogHistoryUseCase:
    return GetDialogHistoryUseCase(
        users=UserRepoSQL(),
        dialogs=DialogRepoSQL(),
        messages=MessageRepoSQL(),
    )


@lru_cache
def get_reset_dialog_usecase() -> ResetDialogUseCase:
    return ResetDialogUseCase(
        users=UserRepoSQL(),
        dialogs=DialogRepoSQL(),
    )


@router.post("/dialogs/message", response_model=SaveMessageResponse)
async def save_message(
    request: SaveMessageRequest,
    usecase: SaveMessageUseCase = Depends(get_save_message_usecase),
) -> SaveMessageResponse:
    try:
        message = usecase.execute(
            tg_id=request.tg_id,
            role=request.role,
            content=request.content,
        )

        return SaveMessageResponse(
            id=message.id,
            dialog_id=message.dialog_id,
            role=message.role,
            content=message.content,
            created_at=message.created_at,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/dialogs/{tg_id}/history", response_model=GetHistoryResponse)
async def get_dialog_history(
    tg_id: int,
    limit: int = 10,
    usecase: GetDialogHistoryUseCase = Depends(get_dialog_history_usecase),
) -> GetHistoryResponse:
    messages = usecase.execute(tg_id=tg_id, limit=limit)

    return GetHistoryResponse(
        messages=[MessageDTO(role=msg.role, content=msg.content) for msg in messages],
        total=len(messages),
    )


@router.post("/dialogs/reset", response_model=ResetDialogResponse)
async def reset_dialog(
    request: ResetDialogRequest,
    usecase: ResetDialogUseCase = Depends(get_reset_dialog_usecase),
) -> ResetDialogResponse:
    try:
        usecase.execute(tg_id=request.tg_id)
        return ResetDialogResponse(
            success=True,
            message="Dialog reset successfully",
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
