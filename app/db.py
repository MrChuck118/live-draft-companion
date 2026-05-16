"""SQLite database setup for local Data Dragon cache."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


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


class CacheEntry(Base):
    """Cached AI output keyed by draft-state hash (MVP-010, T50/T51).

    Single-file SQLite by design (see SPEC_ERRATA ERRATA-007 / INC-011).
    """

    __tablename__ = "cache"

    draft_state_hash: Mapped[str] = mapped_column(String, primary_key=True)
    output_json: Mapped[str] = mapped_column(String, nullable=False)
    model_used: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_utcnow
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class HistoryEntry(Base):
    """Local history of generated suggestions with user feedback (MVP-014, T50/T53)."""

    __tablename__ = "history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=_utcnow
    )
    draft_state_json: Mapped[str] = mapped_column(String, nullable=False)
    output_json: Mapped[str] = mapped_column(String, nullable=False)
    model_used: Mapped[str] = mapped_column(String, nullable=False)
    feedback: Mapped[str] = mapped_column(String, nullable=False, default="unrated")


engine = create_async_engine(DATABASE_URL, future=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db() -> None:
    """Create Data Dragon cache tables if they do not exist."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
