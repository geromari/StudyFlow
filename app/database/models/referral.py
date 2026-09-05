"""Referral model."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.database.models.user import User


class Referral(Base, TimestampMixin):
    __tablename__ = "referrals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    referrer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    referred_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False
    )
    xp_awarded: Mapped[int] = mapped_column(Integer, default=50, nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="completed", nullable=False)

    referrer: Mapped["User"] = relationship("User", foreign_keys=[referrer_id])
    referred: Mapped["User"] = relationship("User", foreign_keys=[referred_id])
