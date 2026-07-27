from datetime import datetime, timezone
from typing import TypedDict
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.common.security import hash_password
from app.data.database import (
    DatabaseNotConfiguredError,
    SessionLocal,
    database_is_configured,
)
from app.data.user_model import User
from app.dtos.user_dto import UserRegisterDto


class UserRecord(TypedDict):
    id: str
    name: str
    lastname: str
    email: str
    number: str
    hashed_password: str
    is_active: bool
    created_at: datetime


class EmailAlreadyExistsError(Exception):
    pass


def register_user(dto: UserRegisterDto) -> UserRecord:
    if not database_is_configured():
        raise DatabaseNotConfiguredError(
            "Configura MYSQL_PASSWORD en el archivo .env",
        )

    email = str(dto.email).lower()

    with SessionLocal() as session:
        email_exists = session.scalar(
            select(User.id).where(User.email == email)
        )

        if email_exists is not None:
            raise EmailAlreadyExistsError()

        user = User(
            id=str(uuid4()),
            name=dto.name,
            lastname=dto.lastname,
            email=email,
            number=dto.number,
            hashed_password=hash_password(dto.password),
            is_active=True,
        )
        session.add(user)

        try:
            session.commit()
        except IntegrityError as error:
            session.rollback()
            raise EmailAlreadyExistsError() from error

        session.refresh(user)
        created_at = user.created_at.replace(tzinfo=timezone.utc)

        return {
            "id": user.id,
            "name": user.name,
            "lastname": user.lastname,
            "email": user.email,
            "number": user.number,
            "hashed_password": user.hashed_password,
            "is_active": user.is_active,
            "created_at": created_at,
        }
