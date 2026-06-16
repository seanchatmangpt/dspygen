from collections.abc import Generator

from sqlalchemy import create_engine, Engine
from sqlmodel import Session, SQLModel

from dspygen.utils.file_tools import data_dir


def _make_engine() -> Engine:
    """Create the SQLAlchemy engine with SQLAlchemy 2.0-style settings."""
    database_url = f"sqlite:///{data_dir('dev.db')}"
    return create_engine(database_url, echo=False, future=True)


# Module-level engine singleton
engine: Engine = _make_engine()


def init_db() -> None:
    """Create all tables defined in the SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a database session and closes it on exit."""
    with Session(engine) as session:
        yield session
