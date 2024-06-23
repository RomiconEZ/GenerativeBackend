from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class ReviewBase(BaseModel):
    text: Annotated[
        str,
        Field(min_length=1, max_length=63206, examples=["This is the content of my review."]),
    ]
    created_by_customer_id: int


class Review(TimestampSchema, ReviewBase, UUIDSchema, PersistentDeletion):
    pass


class ReviewRead(BaseModel):
    id: int
    text: Annotated[
        str,
        Field(min_length=1, max_length=63206, examples=["This is the content of my review."]),
    ]

    created_by_customer_id: int
    created_at: datetime


class ReviewGet(BaseModel):
    text: Annotated[
        str,
        Field(min_length=1, max_length=63206, examples=["This is the content of my review."]),
    ]
    created_by_customer_id: int
    created_at: datetime


class ReviewSend(ReviewGet):
    customer_telegram_username: Annotated[
        str, Field(min_length=1, max_length=60, examples=["tg_name"])
    ]


class ReviewCreate(ReviewBase):
    model_config = ConfigDict(extra="forbid")


class ReviewCreateInternal(ReviewCreate):
    pass


class ReviewUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: Annotated[
        str | None,
        Field(
            min_length=1,
            max_length=63206,
            examples=["This is the updated content of my Review."],
            default=None,
        ),
    ]


class ReviewUpdateInternal(ReviewUpdate):
    pass


class ReviewDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")
    is_deleted: bool
