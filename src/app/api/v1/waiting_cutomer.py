import asyncio
from typing import Annotated, Any, Dict, List

from arq.jobs import Job as ArqJob
from fastapi import APIRouter, Depends, Request, Response, status
from icecream import ic
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import NotFoundException
from ...core.utils import queue
from ...crud.crud_agent import crud_agents
from ...crud.crud_waiting_customers import crud_waiting_customers
from ...schemas.customer import CustomerCreate
from ...schemas.waiting_customers import (
    WaitingCustomersCreateInternal,
    WaitingCustomersRead,
    WaitingCustomersUpdate,
)
from ..dependencies import check_current_customer_else_create

router = APIRouter(tags=["waiting_customer"])

ERROR_SUMMARY_TEXT = "Произошла ошибка на этапе генерации суммаризации"
NO_SUMMARY_TEXT = "История общения с ботом отсутствует."


@router.post("/waiting_customer", response_model=WaitingCustomersRead, status_code=201)
async def add_waiting_customer(
    request: Request,
    customer: CustomerCreate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    context: List[Dict[str, str]] = None,
) -> Response | WaitingCustomersRead:
    await check_current_customer_else_create(customer, db)

    waiting_customer_id = await crud_waiting_customers.get(
        db=db, schema_to_select=WaitingCustomersRead, customer_id=customer.id
    )

    if waiting_customer_id is not None:
        return Response(
            status_code=status.HTTP_409_CONFLICT, content="Waiting customer already exists"
        )

    if context is None or context == []:
        summary = NO_SUMMARY_TEXT
    else:

        job = await queue.pool.enqueue_job("async_gen_summary_using_llm", {"context": context})

        job = ArqJob(job.job_id, queue.pool)

        while True:
            job_info: dict = await job.info()
            if hasattr(job_info, "success"):
                break
            await asyncio.sleep(1)  # Задержка перед следующей проверкой

        # Использование результата, если задача выполнена успешно
        if job_info.success:
            summary = job_info.result
        else:
            summary = ERROR_SUMMARY_TEXT

    waiting_customer_internal = WaitingCustomersCreateInternal(
        customer_id=customer.id, agent_id=None, problem_summary=summary
    )
    created_waiting_customer: WaitingCustomersRead = await crud_waiting_customers.create(
        db=db, object=waiting_customer_internal
    )

    return created_waiting_customer


@router.patch("/waiting_customer")
async def update_waiting_customer(
    request: Request,
    customer_id: int,
    values: WaitingCustomersUpdate,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    waiting_customer_id = await crud_waiting_customers.get(
        db=db, schema_to_select=WaitingCustomersRead, customer_id=customer_id
    )
    if waiting_customer_id is None:
        raise NotFoundException("Waiting customer not found")

    db_agent = await crud_agents.exists(db=db, id=values.agent_id)
    if not db_agent:
        raise NotFoundException("Agent not found")

    await crud_waiting_customers.update(db=db, object=values, customer_id=customer_id)
    return {"message": "Waiting customer updated"}


@router.delete("/waiting_customer")
async def delete_waiting_customer(
    request: Request,
    customer_id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    waiting_customer_id = await crud_waiting_customers.get(
        db=db, schema_to_select=WaitingCustomersRead, customer_id=customer_id
    )
    if waiting_customer_id is None:
        raise NotFoundException("Waiting customer not found")

    await crud_waiting_customers.delete(db=db, customer_id=customer_id)
    return {"message": f"Waiting customer {customer_id} deleted"}


@router.get("/waiting_customer", response_model=tuple[WaitingCustomersRead, int])
async def get_waiting_customer(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> tuple[WaitingCustomersRead | None, int]:
    stmt = await crud_waiting_customers.select(
        schema_to_select=WaitingCustomersRead, sort_columns="created_at", sort_orders="asc"
    )
    # Добавляем limit к запросу вручную после его создания
    limited_stmt = stmt.limit(1)
    # Выполняем запрос и получаем результат
    result = await db.execute(limited_stmt)

    customer_with_longest_waiting_time: WaitingCustomersRead | None = result.first()
    ic(customer_with_longest_waiting_time)
    if customer_with_longest_waiting_time:
        count = int(await crud_waiting_customers.count(db))
        ic(count)
        return customer_with_longest_waiting_time, count
    else:
        return None, 0


@router.get("/waiting_customer_count", response_model=int)
async def get_count_waiting_customer(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> int:
    count = await crud_waiting_customers.count(db)

    return count
