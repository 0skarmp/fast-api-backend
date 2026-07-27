import asyncio

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.controllers.auth_controller import (
    EmailAlreadyExistsError,
    register_user,
)
from app.data.database import DatabaseNotConfiguredError
from app.dtos.user_dto import (
    UserRegisterDto,
    UserRegisterResponseDto,
    UserResponseDto,
)

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
)


@router.post(
    "/register",
    response_model=UserRegisterResponseDto,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "El email ya está registrado",
        },
    },
)
async def register(dto: UserRegisterDto) -> UserRegisterResponseDto:
    try:
        user = await asyncio.to_thread(register_user, dto)
    except EmailAlreadyExistsError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email ya está registrado",
        ) from error
    except DatabaseNotConfiguredError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        ) from error
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        ) from error

    return UserRegisterResponseDto(
        message="Usuario registrado correctamente",
        user=UserResponseDto(
            id=user["id"],
            name=user["name"],
            lastname=user["lastname"],
            email=user["email"],
            number=user["number"],
            is_active=user["is_active"],
            created_at=user["created_at"],
        ),
    )
