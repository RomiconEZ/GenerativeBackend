from typing import Annotated

from ...api.dependencies import get_current_superagent
from ...core.config import settings
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from ...crud.crud_agent import crud_agents
from ...schemas.agent import AgentRead, AgentCreate, AgentCreateInternal, AgentUpdate
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from io import BytesIO
import pandas as pd
from fastapi.responses import StreamingResponse

router = APIRouter(tags=["agent"])


@router.post("/agent", response_model=AgentRead,
             status_code=201)
async def write_agent(
        request: Request, self_agent_id: int,
        new_agent: AgentCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> AgentRead:
    await get_current_superagent(self_agent_id, db)

    id_row = await crud_agents.exists(db=db, id=new_agent.id)
    if id_row:
        raise DuplicateValueException("ID is already registered")

    agent_internal_dict = new_agent.model_dump()
    agent_internal = AgentCreateInternal(**agent_internal_dict)
    created_agent: AgentRead = await crud_agents.create(db=db, object=agent_internal)
    return created_agent


@router.patch("/agent/{updated_agent_id}")
async def update_tour(
        request: Request,
        updated_agent_id: int,
        updated_agent: AgentUpdate,
        db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_agent_id = await crud_agents.get(db=db, schema_to_select=AgentRead, id=updated_agent_id)
    if db_agent_id is None:
        raise NotFoundException("Agent not found")

    await crud_agents.update(db=db, object=updated_agent, id=updated_agent_id)
    return {"message": "Agent updated"}


@router.get("/agents", response_class=StreamingResponse)
async def get_all_agents(
        request: Request, self_agent_id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
):
    # Проверка прав текущего пользователя
    await get_current_superagent(self_agent_id, db)

    # Получение данных агентов
    agents_data = await crud_agents.get_multi(
        db=db,
        offset=0,
        limit=settings.INT_MAX_AGENTS,
        schema_to_select=AgentRead,
        return_as_model=True,  # Убедитесь, что данные возвращаются как модели Pydantic
        is_deleted=False
    )

    # Конвертация данных в DataFrame
    df = pd.DataFrame([agent.dict() for agent in agents_data['data']])

    # Сохранение DataFrame в Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    # Создание и отправка StreamingResponse
    response = StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=agents.xlsx"}
    )
    return response


@router.delete("/agent/{delete_agent_id}")
async def erase_db_agent(
        request: Request,
        self_agent_id: int,
        delete_agent_id: int,
        db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    await get_current_superagent(self_agent_id, db)

    db_agent = await crud_agents.exists(db=db, id=delete_agent_id)
    if not db_agent:
        raise NotFoundException("Agent not found")

    await crud_agents.db_delete(db=db, id=delete_agent_id)
    return {"message": f"Agent {delete_agent_id} deleted from the database"}
