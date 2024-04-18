from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class AgentBase(BaseModel):
    id: int
    name: Annotated[str | None, Field(min_length=1, max_length=30, examples=["Name"], default=None)]
    surname: Annotated[str | None, Field(min_length=1, max_length=50, examples=["Surname"], default=None)]
    patronymic: Annotated[str | None, Field(min_length=1, max_length=40, examples=["Patronymic"], default=None)]

    username_telegram: Annotated[str, Field(min_length=1, max_length=60, examples=["tg_name"], default=None)]

    email: Annotated[EmailStr | None, Field(examples=["agent.agent@example.com"], default=None)]


class Agent(TimestampSchema, AgentBase, UUIDSchema, PersistentDeletion):
    is_superuser: bool = False
    tier_id: int | None = None


class AgentRead(AgentBase):

    tier_id: int | None


class AgentCreate(AgentBase):
    model_config = ConfigDict(extra="forbid")


class AgentCreateInternal(AgentCreate):
    pass


class AgentUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[str | None, Field(min_length=1, max_length=30, examples=["Name"], default=None)]
    surname: Annotated[str | None, Field(min_length=1, max_length=50, examples=["Surname"], default=None)]
    patronymic: Annotated[str | None, Field(min_length=1, max_length=40, examples=["Patronymic"], default=None)]

    username_telegram: Annotated[str | None, Field(min_length=1, max_length=60, examples=["tg_name"], default=None)]

    email: Annotated[EmailStr | None, Field(examples=["agent.agent@example.com"], default=None)]


class AgentUpdateInternal(AgentUpdate):
    updated_at: datetime


class AgentTierUpdate(BaseModel):
    tier_id: int


class AgentDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class AgentRestoreDeleted(BaseModel):
    is_deleted: bool
