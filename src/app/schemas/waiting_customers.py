from datetime import datetime
from typing import Annotated, Optional

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


class WaitingCustomersGet(BaseModel):
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
    customer_telegram_username: Annotated[
        str, Field(min_length=1, max_length=60, examples=["tg_name"])
    ]
    customer_name: Annotated[
        str | None, Field(min_length=1, max_length=30, examples=["Name"], default=None)
    ]
    customer_surname: Annotated[
        str | None, Field(min_length=1, max_length=50, examples=["Surname"], default=None)
    ]
    customer_patronymic: Annotated[
        str | None, Field(min_length=1, max_length=40, examples=["Patronymic"], default=None)
    ]
    created_at: datetime


class WaitingCustomersCreate(WaitingCustomersBase):
    model_config = ConfigDict(extra="forbid")


class WaitingCustomersCreateInternal(WaitingCustomersCreate):
    pass


class WaitingCustomersUpdate(BaseModel):
    agent_id: Annotated[Optional[int], Field(default=None)]
    model_config = ConfigDict(extra="forbid")


class WaitingCustomersUpdateInternal(WaitingCustomersUpdate):
    updated_at: datetime


class WaitingCustomersDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")
    pass
