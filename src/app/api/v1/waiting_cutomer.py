import asyncio
from typing import Annotated, Dict, List

from arq.jobs import Job as ArqJob
from fastapi import APIRouter, Depends, HTTPException, Request, status
from icecream import ic
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import NotFoundException
from ...core.utils import queue
from ...crud.crud_agent import crud_agents
from ...crud.crud_customer import crud_customers
from ...crud.crud_waiting_customers import crud_waiting_customers
from ...schemas.customer import CustomerCreate, CustomerRead
from ...schemas.waiting_customers import (
    WaitingCustomersCreateInternal,
    WaitingCustomersGet,
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

    if values.agent_id is not None:
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


@router.get("/waiting_customer", response_model=tuple[WaitingCustomersGet | None, int])
async def get_waiting_customer(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> tuple[WaitingCustomersGet, int] | tuple[None, int]:
    stmt = await crud_waiting_customers.select(
        schema_to_select=WaitingCustomersRead,
        sort_columns="created_at",
        sort_orders="asc",
        agent_id=None,
        limit=1,
    )
    # Выполняем запрос и получаем результат
    result = await db.execute(stmt)

    customer_with_longest_waiting_time: WaitingCustomersRead | None = result.first()

    if customer_with_longest_waiting_time:
        # Получаем выбранного клиента как словарь
        selected_customer_dict = await crud_customers.get(
            db=db, id=customer_with_longest_waiting_time.customer_id, is_deleted=False
        )

        if not selected_customer_dict:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
            )

        # Преобразуем результат к объекту `CustomerRead`
        selected_customer = CustomerRead(**selected_customer_dict)

        # Создаем экземпляр WaitingCustomersGet с объединенными данными
        waiting_customer = WaitingCustomersGet(
            customer_id=customer_with_longest_waiting_time.customer_id,
            agent_id=customer_with_longest_waiting_time.agent_id,
            problem_summary=customer_with_longest_waiting_time.problem_summary,
            created_at=customer_with_longest_waiting_time.created_at,
            customer_telegram_username=selected_customer.username_telegram,
            customer_name=selected_customer.name,
            customer_surname=selected_customer.surname,
            customer_patronymic=selected_customer.patronymic,
        )

        count = int(await crud_waiting_customers.count(db))
        return waiting_customer, count
    else:
        return None, 0


@router.get("/waiting_customer_count", response_model=int)
async def get_count_waiting_customer(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> int:
    count = await crud_waiting_customers.count(db)

    return count
