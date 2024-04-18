from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class TourBase(BaseModel):
    title: Annotated[str, Field(min_length=2, max_length=30, examples=["This is my Tour"])]
    text: Annotated[str, Field(min_length=1, max_length=63206, examples=["This is the content of my Tour."])]
    created_by_agent_id: int


class Tour(TimestampSchema, TourBase, UUIDSchema, PersistentDeletion):
    created_by_agent_id: int


class TourRead(BaseModel):
    id: int
    title: Annotated[str, Field(min_length=2, max_length=30, examples=["This is my Tour"])]
    text: Annotated[str, Field(min_length=1, max_length=63206, examples=["This is the content of my Tour."])]
    created_by_agent_id: int
    last_updated_by_agent_id: int | None = None

    created_at: datetime


class TourCreate(TourBase):
    model_config = ConfigDict(extra="forbid")


class TourCreateInternal(TourCreate):
    last_updated_by_agent_id: None = None
    pass


class TourUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Annotated[str | None, Field(min_length=2, max_length=30, examples=["This is my updated Tour"], default=None)]
    text: Annotated[
        str | None,
        Field(min_length=1, max_length=63206, examples=["This is the updated content of my Tour."], default=None),
    ]
    last_updated_by_agent_id: int


class TourUpdateInternal(TourUpdate):
    updated_at: datetime


class TourDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime
