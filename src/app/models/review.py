import uuid as uuid_pkg
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..core.db.database import Base
from ..core.timezone import UTC_PLUS_3


class Review(Base):
    __tablename__ = "review"

    id: Mapped[int] = mapped_column(
        "id",
        BigInteger,
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )
    created_by_customer_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("customer.id"), index=True
    )
    text: Mapped[str] = mapped_column(String(63206))
    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        default_factory=uuid_pkg.uuid4, primary_key=True, unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC_PLUS_3)
    )
