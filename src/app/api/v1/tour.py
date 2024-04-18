from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from ..dependencies import get_current_superagent
from ...core.config import settings
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException

from ...crud.crud_tour import crud_tours
import pandas as pd
from ...schemas.tour import TourCreate, TourRead, TourUpdate, TourCreateInternal
from io import BytesIO

router = APIRouter(tags=["tour"])


@router.post("/tour", response_model=TourRead, status_code=201)
async def add_tour(
        request: Request, tour: TourCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> TourRead:
    title = await crud_tours.exists(db=db, title=tour.title)
    if title:
        raise DuplicateValueException("Tour title is already registered")

    tour_internal_dict = tour.model_dump()

    tour_internal = TourCreateInternal(**tour_internal_dict)
    created_tour: TourRead = await crud_tours.create(db=db, object=tour_internal)

    return created_tour


@router.get("/tours", response_class=StreamingResponse)
async def get_all_tours(
        request: Request, db: Annotated[AsyncSession, Depends(async_get_db)]
):
    # Получение данных
    reviews_data = await crud_tours.get_multi(
        db=db,
        offset=0,
        limit=settings.INT_MAX_TOUR,
        schema_to_select=TourRead,
        return_as_model=True,  # Данные возвращаются как модели Pydantic
        is_deleted=False
    )

    # Конвертация данных в DataFrame
    df = pd.DataFrame([tour.dict() for tour in reviews_data['data']])

    # Преобразование datetime с временной зоной в без временной зоны
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_convert(None) + timedelta(hours=settings.TIME_ZONE)

    # Сохранение DataFrame в Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    # Создание и отправка StreamingResponse
    response = StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=tours.xlsx"}
    )
    return response


@router.patch("/tour/{tour_id}")
async def update_tour(
        request: Request,
        tour_id: int,
        updated_tour: TourUpdate,
        db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_tour_id = await crud_tours.get(db=db, schema_to_select=TourRead, id=tour_id)
    if db_tour_id is None:
        raise NotFoundException("Tour not found")

    await crud_tours.update(db=db, object=updated_tour, id=tour_id)
    return {"message": "Tour updated"}


@router.delete("/tour/{tour_id}")
async def delete_tour(
        request: Request,
        tour_id: int,
        db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_tour_id = await crud_tours.get(db=db, schema_to_select=TourRead, id=tour_id)
    if db_tour_id is None:
        raise NotFoundException("Tour not found")

    await crud_tours.delete(db=db, id=tour_id)
    return {"message": "Tour deleted"}


@router.delete("/tours")
async def delete_all_tours(request: Request,
                           self_agent_id: int,
                           db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict[str, str]:
    await get_current_superagent(self_agent_id, db)

    await crud_tours.delete(db=db, allow_multiple=True)
    return {"message": "All tours deleted"}
