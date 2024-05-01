from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class WaitingCustomersBase(BaseModel):
    customer_id: int
    agent_id: Annotated[int | None, Field(default=None)]
    problem_summary: Annotated[
        str | None,
        Field(
            min_length=1,
            max_length=63206,
            examples=["This is the summary of the " "problem."],
            default=None,
        ),
    ]


class WaitingCustomers(TimestampSchema, WaitingCustomersBase, UUIDSchema, PersistentDeletion):
    pass


class WaitingCustomersRead(BaseModel):
    id: int
    agent_id: Annotated[int | None, Field(default=None)]
    customer_id: Annotated[int, Field(default=None)]
    problem_summary: Annotated[
        str,
        Field(
            min_length=1,
            max_length=63206,
            examples=["This is the summary of the " "problem."],
            default=None,
        ),
    ]
    created_at: datetime


class WaitingCustomersCreate(WaitingCustomersBase):
    model_config = ConfigDict(extra="forbid")


class WaitingCustomersCreateInternal(WaitingCustomersCreate):
    pass


class WaitingCustomersUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    agent_id: Annotated[int | None, Field(default=None)]


class WaitingCustomersUpdateInternal(WaitingCustomersUpdate):
    updated_at: datetime


class WaitingCustomersDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")
    pass
