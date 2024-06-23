import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from ..core.timezone import UTC_PLUS_3
from ..core.db.database import Base


class WaitingCustomers(Base):
    __tablename__ = "waiting_customers"
    id: Mapped[int] = mapped_column(
        "id", BigInteger, autoincrement=True, nullable=False, unique=True, primary_key=True, init=False
    )

    agent_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("agent.id"), nullable=True, init=True
    )
    customer_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("customer.id"), nullable=False, unique=True, init=True
    )

    problem_summary: Mapped[str] = mapped_column(String(63206), nullable=True)
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        default_factory=uuid_pkg.uuid4, primary_key=True, unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC_PLUS_3)
    )
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
