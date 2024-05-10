import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..core.timezone import UTC_PLUS_3
from ..core.db.database import Base


class CustomersWaitingTour(Base):
    __tablename__ = "customers_waiting_tour"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True, init=False
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer.id"), nullable=False, init=True
    )
    tour_id: Mapped[int] = mapped_column(ForeignKey("tour.id"), nullable=False, init=True)
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        default_factory=uuid_pkg.uuid4, primary_key=True, unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC_PLUS_3)
    )
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
