import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.timezone import UTC_PLUS_3
from ..core.db.database import Base


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column("id", nullable=False, unique=True, primary_key=True)

    name: Mapped[str] = mapped_column(String(30), nullable=True)
    surname: Mapped[str] = mapped_column(String(50), nullable=True)
    patronymic: Mapped[str] = mapped_column(String(40), nullable=True)

    username_telegram: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=True
    )
    email: Mapped[str] = mapped_column(String(50), unique=False, index=False, nullable=True)

    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        default_factory=uuid_pkg.uuid4, primary_key=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC_PLUS_3)
    )
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)

    tier_id: Mapped[int | None] = mapped_column(
        ForeignKey("tier.id"), index=True, default=None, init=False
    )
