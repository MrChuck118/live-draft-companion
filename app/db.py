"""SQLite database setup for local Data Dragon cache."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


DATABASE_URL = "sqlite+aiosqlite:///data_dragon.db"


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


class Champion(Base):
    """Cached champion static data from Data Dragon."""

    __tablename__ = "champions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    key: Mapped[str] = mapped_column(String, nullable=False)
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    image_url: Mapped[str] = mapped_column(String, nullable=False)


class Item(Base):
    """Cached item static data from Data Dragon."""

    __tablename__ = "items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    stats: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)


class Rune(Base):
    """Cached keystone rune static data from Data Dragon."""

    __tablename__ = "runes"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    key: Mapped[str] = mapped_column(String, nullable=False)
    tree: Mapped[str] = mapped_column(String, nullable=False)
    tree_key: Mapped[str] = mapped_column(String, nullable=False)
    icon_url: Mapped[str] = mapped_column(String, nullable=False)


class Meta(Base):
    """Key-value metadata for cache state, such as the current patch."""

    __tablename__ = "meta"

    key: Mapped[str] = mapped_column(String, primary_key=True)
    value: Mapped[str] = mapped_column(String, nullable=False)


engine = create_async_engine(DATABASE_URL, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db() -> None:
    """Create Data Dragon cache tables if they do not exist."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
