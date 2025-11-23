from functools import lru_cache

from fastapi import Depends, HTTPException

from app.adapters.dto.user import CreateUserRequest, CreateUserResponse
from app.application.user import CreateUserUseCase
from app.domain.exceptions import UsernameAlreadyExistsError
from app.infrastructure.repos.user import UserRepoSQL

from .common import router


@lru_cache
def get_create_user_usecase() -> CreateUserUseCase:
    return CreateUserUseCase(UserRepoSQL())


@router.post("/user/create")
async def create_user(
    request: CreateUserRequest,
    usecase: CreateUserUseCase = Depends(get_create_user_usecase),
) -> CreateUserResponse:
    try:
        user = usecase.execute(
            tg_id=request.tg_id,
            first_name=request.first_name,
            last_name=request.last_name,
            is_bot=request.is_bot,
            language_code=request.language_code,
            username=request.username,
        )

        return CreateUserResponse(
            id=user.id,
            tg_id=user.tg_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_bot=user.is_bot,
            language_code=user.language_code,
            created_at=user.created_at,
        )
    except UsernameAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
