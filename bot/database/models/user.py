from __future__ import annotations

from aiogram import html
from aiogram.types import User
from aiogram.utils.link import create_tg_link
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, Int64, TimestampMixin


class DBUser(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)

    @classmethod
    def from_aiogram(cls, user: User) -> DBUser:
        return DBUser(
            id=user.id,
            name=user.full_name,
        )
