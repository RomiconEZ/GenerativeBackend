from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.timezone import UTC_PLUS_3
from ..core.db.database import Base


class Tier(Base):
    __tablename__ = "tier"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False
    )
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC_PLUS_3)
    )
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
