from datetime import timedelta
from io import BytesIO
from typing import Annotated

import pandas as pd
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from icecream import ic
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.config import settings
from ...core.db.database import async_get_db
from ...crud.crud_customer import crud_customers
from ...crud.crud_review import crud_reviews
from ...models.customer import Customer
from ...schemas.customer import CustomerCreateInternal, CustomerRead, CustomerIdUsername
from ...schemas.review import ReviewCreate, ReviewCreateInternal, ReviewRead, ReviewGet
from ..dependencies import get_current_superagent

router = APIRouter(tags=["review"])


@router.get("/reviews", response_class=StreamingResponse)
async def get_all_reviews(
        request: Request, db: Annotated[AsyncSession, Depends(async_get_db)]
):
    reviews_data = await crud_reviews.get_multi_joined(
        db, join_model=Customer,
        schema_to_select=ReviewGet,
        join_schema_to_select=CustomerIdUsername,
        join_type='left',
        sort_columns='created_at',
        sort_orders='asc'
    )

    # Конвертация данных в DataFrame
    df = pd.DataFrame([review for review in reviews_data["data"]])

    if reviews_data['total_count'] > 0:
        df.drop(columns=["id"], inplace=True)

        # Set the desired order of columns
        desired_order = ["created_at", "username_telegram", "created_by_customer_id", "text"]
        # Reorder the columns
        df = df[desired_order]

        # Преобразование datetime с временной зоной в без временной зоны
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_convert(None) + timedelta(hours=settings.TIME_ZONE)

    # Сохранение DataFrame в Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    # Создание и отправка StreamingResponse
    response = StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=reviews.xlsx"},
    )
    return response


@router.post("/review", response_model=ReviewRead, status_code=201)
async def write_review(
        request: Request,
        review: ReviewCreate,
        customer_telegram_username: str,
        db: Annotated[AsyncSession, Depends(async_get_db)],
) -> ReviewRead:
    customer_row = await crud_customers.exists(db=db, id=review.created_by_customer_id)
    if not customer_row:
        customer_internal_dict = {
            "id": review.created_by_customer_id,
            "username_telegram": customer_telegram_username,
        }
        customer_internal = CustomerCreateInternal(**customer_internal_dict)
        created_customer: CustomerRead = await crud_customers.create(
            db=db, object=customer_internal
        )

    review_internal_dict = review.model_dump()
    review_internal = ReviewCreateInternal(**review_internal_dict)

    created_review: ReviewRead = await crud_reviews.create(db=db, object=review_internal)
    return created_review


@router.delete("/reviews")
async def delete_db_all_reviews(
        request: Request, self_agent_id: int, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    # Проверка прав текущего пользователя
    await get_current_superagent(self_agent_id, db)

    await crud_reviews.db_delete(db=db, allow_multiple=True)
    return {"message": "All reviews deleted"}
