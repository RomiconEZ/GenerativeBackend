import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base
from ..core.timezone import UTC_PLUS_3


class Agent(Base):
    __tablename__ = "agent"

    id: Mapped[int] = mapped_column(
        "id", BigInteger, unique=True, primary_key=True, nullable=False
    )

    name: Mapped[str] = mapped_column(String(30), nullable=True)
    surname: Mapped[str] = mapped_column(String(50), nullable=True)
    patronymic: Mapped[str] = mapped_column(String(40), nullable=True)

    username_telegram: Mapped[str] = mapped_column(
        String(60), unique=True, index=True, nullable=False
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
    is_superuser: Mapped[bool] = mapped_column(default=False)

    tier_id: Mapped[int | None] = mapped_column(
        ForeignKey("tier.id"), index=True, default=None, init=False
    )
