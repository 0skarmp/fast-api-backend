import re

from sqlalchemy import URL, create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.common.config import get_settings

settings = get_settings()


class DatabaseNotConfiguredError(RuntimeError):
    pass


class Base(DeclarativeBase):
    pass


def _create_mysql_url(database: str | None) -> URL:
    return URL.create(
        drivername="mysql+pymysql",
        username=settings.mysql_user,
        password=settings.mysql_password,
        host=settings.mysql_host,
        port=settings.mysql_port,
        database=database,
        query={"charset": "utf8mb4"},
    )


engine: Engine = create_engine(
    _create_mysql_url(settings.mysql_database),
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def database_is_configured() -> bool:
    return bool(settings.mysql_password)


def init_database() -> None:
    if not database_is_configured():
        raise DatabaseNotConfiguredError(
            "Configura MYSQL_PASSWORD en el archivo .env",
        )

    if not re.fullmatch(r"[A-Za-z0-9_]+", settings.mysql_database):
        raise ValueError("MYSQL_DATABASE contiene caracteres no permitidos")

    server_engine = create_engine(
        _create_mysql_url(database=None),
        pool_pre_ping=True,
    )

    try:
        with server_engine.begin() as connection:
            connection.execute(
                text(
                    f"CREATE DATABASE IF NOT EXISTS "
                    f"`{settings.mysql_database}` "
                    "CHARACTER SET utf8mb4 "
                    "COLLATE utf8mb4_unicode_ci"
                )
            )
    finally:
        server_engine.dispose()

    # Importa los modelos antes de crear las tablas.
    from app.data import user_model  # noqa: F401

    Base.metadata.create_all(bind=engine)
