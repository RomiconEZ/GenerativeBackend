from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class CustomersWaitingTourBase(BaseModel):
    customer_id: int
    tour_id: int


class CustomersWaitingTour(TimestampSchema, CustomersWaitingTourBase, UUIDSchema, PersistentDeletion):
    pass


class CustomersWaitingTourRead(BaseModel):
    id: int
    customer_id: Annotated[int | None, Field(default=None)]
    tour_id: Annotated[int | None, Field(default=None)]

    created_at: datetime


class CustomersWaitingTourCreate(CustomersWaitingTourBase):
    model_config = ConfigDict(extra="forbid")


class CustomersWaitingTourCreateInternal(CustomersWaitingTourCreate):
    pass


class CustomersWaitingTourUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tour_id: Annotated[int | None, Field(default=None)]


class CustomersWaitingTourUpdateInternal(CustomersWaitingTourUpdate):
    updated_at: datetime


class CustomersWaitingTourDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")
    pass
