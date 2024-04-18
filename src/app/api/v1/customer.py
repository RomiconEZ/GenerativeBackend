import os
from typing import Any, Dict
from typing import Annotated

from arq.jobs import Job as ArqJob
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...api.dependencies import rate_limiter, check_current_customer_else_create
from ...core.utils import queue
from ...schemas.customer import CustomerCreate
from ...schemas.job import Job
from ...core.db.database import async_get_db
from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi import HTTPException
from fastapi import BackgroundTasks

from ...crud.crud_customer import crud_customers
from ...crud.crud_agent import crud_agents
from ...crud.crud_customers_waiting_tour import crud_customers_waiting_tour
from ...crud.crud_review import crud_reviews
from ...crud.crud_tour import crud_tours
from ...crud.crud_waiting_customers import crud_waiting_customers

router = APIRouter(prefix="/customer", tags=["customer"])


@router.post("/answer_generation/{customer_id}", response_model=Job | None, status_code=201,
             dependencies=[Depends(rate_limiter)])
async def create_task_for_answer_generation(
        customer: CustomerCreate,
        human_input: str,
        db: Annotated[AsyncSession, Depends(async_get_db)],
        context: Dict[str, Any] = None) -> dict[str, str] | None:
    """Create a new background task.

    Parameters
    ----------
    customer
    db
    context
    human_input

    Returns
    -------
    dict[str, str]
        A dictionary containing the ID of the created task.
    """
    await check_current_customer_else_create(customer, db)

    if human_input:
        job = await queue.pool.enqueue_job("async_gen_ans_using_llm",
                                           {"human_input": human_input, "context": context})  # type: ignore
        return {"id": job.job_id}
    else:
        return None


@router.post("/audio_generation/{customer_id}", response_model=Job | None, status_code=201,
             dependencies=[Depends(rate_limiter)])
async def create_task_for_audio_generation(
        customer: CustomerCreate,
        text: str,
        db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str] | None:
    """Create a new background task.

    Parameters
    ----------
    customer
    db
    context
    human_input

    Returns
    -------
    dict[str, str]
        A dictionary containing the ID of the created task.
    """
    await check_current_customer_else_create(customer, db)

    if text:
        job = await queue.pool.enqueue_job("async_gen_audio_for_text",
                                           {"text": text, "customer_id": customer.id})  # type: ignore
        return {"id": job.job_id}
    else:
        return None


@router.get("/answer_generation/{task_id}")
async def get_task_for_answer_generation(task_id: str) -> str:
    """Get information about a specific background task.

    Parameters
    ----------
    task_id: str
        The ID of the task.

    Returns
    -------
    Optional[dict[str, Any]]
        A dictionary containing information about the task if found, or None otherwise.
    """
    job = ArqJob(task_id, queue.pool)
    job_info: dict = await job.info()

    if getattr(job_info, 'success', False):
        try:
            return job_info.result['history'][-1]["content"]
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Request understood but cannot be processed due to logical errors."
            )
    else:
        raise HTTPException(status_code=404, detail="Task not completed or failed.")

    return vars(job_info)


def remove_file(path):
    os.remove(path)


@router.get("/audio_generation/{task_id}")
async def get_task_for_audio_generation(task_id: str, background_tasks: BackgroundTasks) -> FileResponse:
    """Get information about a specific background task and return the generated audio file if available.

    Parameters:
    task_id : str
        The ID of the task.

    Returns:
    FileResponse | None
        A file response that lets the client download the generated audio file, or None if no file is found.
    """
    job = ArqJob(task_id, queue.pool)
    job_info = await job.info()

    if getattr(job_info, 'success', False):

        path_to_gen_audio = job_info.result
        # Добавление задачи на удаление файла после отправки ответа, передаем путь к файлу в функцию
        background_tasks.add_task(remove_file, path_to_gen_audio)
        try:
            return FileResponse(path_to_gen_audio, media_type="audio/ogg", filename="generated_audio.ogg")
        except FileNotFoundError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Request understood but cannot be processed due to logical errors."
            )
    else:
        raise HTTPException(status_code=404, detail="Task not completed or failed.")
