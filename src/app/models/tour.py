import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base


class Tour(Base):
    __tablename__ = "tour"

    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    title: Mapped[str] = mapped_column(String(30), unique=True)
    text: Mapped[str] = mapped_column(String(63206))

    created_by_agent_id: Mapped[int] = mapped_column(ForeignKey("agent.id"))
    last_updated_by_agent_id: Mapped[int] = mapped_column(ForeignKey("agent.id"), nullable=True)

    uuid: Mapped[uuid_pkg.UUID] = mapped_column(default_factory=uuid_pkg.uuid4, primary_key=True, unique=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
