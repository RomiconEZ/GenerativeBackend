from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
import uuid as uuid_pkg

from ..core.db.database import Base


class WaitingCustomers(Base):
    __tablename__ = "waiting_customers"
    id: Mapped[int] = mapped_column("id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False)

    agent_id: Mapped[int | None] = mapped_column(ForeignKey("agent.id"), nullable=True, init=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"), nullable=False, unique=True, init=True)

    problem_summary: Mapped[str] = mapped_column(String(63206), nullable=True)
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(default_factory=uuid_pkg.uuid4, primary_key=True, unique=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
