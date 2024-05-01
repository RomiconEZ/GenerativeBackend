from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastcrud.exceptions.http_exceptions import NotFoundException
from icecream import ic
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import settings
from ..core.db.database import async_get_db
from ..core.exceptions.http_exceptions import RateLimitException
from ..core.logger import logging
from ..core.utils.rate_limit import is_rate_limited
from ..crud.crud_agent import crud_agents
from ..crud.crud_customer import crud_customers
from ..crud.crud_rate_limit import crud_rate_limits
from ..crud.crud_tier import crud_tiers
from ..schemas.agent import AgentRead
from ..schemas.customer import CustomerCreate, CustomerCreateInternal, CustomerRead
from ..schemas.rate_limit import sanitize_path

logger = logging.getLogger(__name__)

DEFAULT_LIMIT = settings.DEFAULT_RATE_LIMIT_LIMIT
DEFAULT_PERIOD = settings.DEFAULT_RATE_LIMIT_PERIOD


async def get_current_customer(
    customer_id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> CustomerRead | None:
    customer: CustomerRead | None = await crud_customers.get(
        db=db, id=customer_id, is_deleted=False
    )

    if customer:
        return customer
    else:
        return None


async def check_current_customer_else_create(
    customer: CustomerCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> CustomerRead:

    customer_row: CustomerRead | None = await crud_customers.get(
        db=db, id=customer.id, is_deleted=False
    )
    if not customer_row:
        customer_internal_dict = customer.model_dump()
        customer_internal = CustomerCreateInternal(**customer_internal_dict)
        created_customer: CustomerRead = await crud_customers.create(
            db=db, object=customer_internal
        )
        return created_customer
    else:
        return customer_row


async def get_current_agent(
    agent_id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> AgentRead | None:
    agent: AgentRead | None = await crud_agents.get(db=db, id=agent_id, is_deleted=False)

    if agent:
        return agent
    else:
        raise NotFoundException("Your agent account doesn't exist")


async def get_current_superagent(
    agent_id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> AgentRead:
    agent: AgentRead = await get_current_agent(agent_id, db)
    if not agent["is_superuser"]:
        raise HTTPException(status_code=403, detail="You do not have enough privileges.")
    return agent


async def rate_limiter(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], customer_id: int
) -> None:
    user = await get_current_customer(customer_id=customer_id, db=db)
    path = sanitize_path(request.url.path)
    if user:
        user_id = user["id"]
        tier = await crud_tiers.get(db, id=user["tier_id"])
        if tier:
            rate_limit = await crud_rate_limits.get(db=db, tier_id=tier["id"], path=path)
            if rate_limit:
                limit, period = rate_limit["limit"], rate_limit["period"]
            else:
                logger.warning(
                    f"User {user_id} with tier '{tier['name']}' has no specific rate limit for path '{path}'. \
                        Applying default rate limit."
                )
                limit, period = DEFAULT_LIMIT, DEFAULT_PERIOD
        else:
            logger.warning(
                f"User {user_id} has no assigned tier. Applying default rate limit."
            )
            limit, period = DEFAULT_LIMIT, DEFAULT_PERIOD
    else:
        user_id = request.client.host
        limit, period = DEFAULT_LIMIT, DEFAULT_PERIOD

    is_limited = await is_rate_limited(
        db=db, user_id=user_id, path=path, limit=limit, period=period
    )
    if is_limited:
        raise RateLimitException("Rate limit exceeded.")
