import asyncio
import logging
import uuid
from datetime import UTC, datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    insert,
    select,
)
from sqlalchemy.dialects.postgresql import UUID

from ..app.core.config import settings
from ..app.core.db.database import AsyncSession, async_engine, local_session
from ..app.models.agent import Agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_first_user(session: AsyncSession) -> None:
    try:
        name = settings.ADMIN_AGENT_NAME
        surname = settings.ADMIN_AGENT_SURNAME
        agent_id = int(settings.ADMIN_AGENT_ID)
        email = settings.ADMIN_AGENT_EMAIL
        username_telegram = settings.ADMIN_AGENT_USERNAME

        query = select(Agent).filter_by(id=agent_id)
        result = await session.execute(query)
        agent_admin = result.scalar_one_or_none()

        if agent_admin is None:
            metadata = MetaData()
            user_table = Table(
                "agent",
                metadata,
                Column("id", Integer, primary_key=True, nullable=False),
                Column("name", String(30), nullable=False),
                Column("surname", String(50), nullable=False),
                Column("patronymic", String(40), nullable=False),
                Column(
                    "username_telegram", String(60), nullable=False, unique=True, index=True
                ),
                Column("email", String(50), nullable=True, unique=False, index=False),
                Column(
                    "uuid",
                    UUID(as_uuid=True),
                    primary_key=True,
                    default=uuid.uuid4,
                    unique=True,
                ),
                Column(
                    "created_at",
                    DateTime(timezone=True),
                    default=lambda: datetime.now(UTC),
                    nullable=False,
                ),
                Column("updated_at", DateTime),
                Column("deleted_at", DateTime),
                Column("is_deleted", Boolean, default=False, index=True),
                Column("is_superuser", Boolean, default=False),
                Column("tier_id", Integer, ForeignKey("tier.id"), index=True),
            )

            data = {
                "name": name,
                "surname": surname,
                "id": agent_id,
                "email": email,
                "username_telegram": username_telegram,
                "is_superuser": True,
            }

            stmt = insert(user_table).values(data)
            async with async_engine.connect() as conn:
                await conn.execute(stmt)
                await conn.commit()

            logger.info(f"Admin agent {username_telegram} created successfully.")

        else:
            logger.info(f"Admin agent {username_telegram} already exists.")

    except Exception as e:
        raise


async def main():
    retry_attempts = 4
    async with local_session() as session:
        for attempt in range(retry_attempts):
            try:
                await create_first_user(session)
                break  # Если выполнение успешно, выйти из цикла
            except Exception as e:
                logger.error(f"Attempt {attempt + 1}/{retry_attempts} - Error creating admin agent: {e}")
                if attempt < retry_attempts - 1:
                    await asyncio.sleep(4)  # Задержка перед повторной попыткой
                else:
                    logger.error("Exceeded maximum retry attempts.")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
