from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class CustomerBase(BaseModel):
    id: int
    name: Annotated[
        str | None, Field(min_length=1, max_length=30, examples=["Name"], default=None)
    ]
    surname: Annotated[
        str | None, Field(min_length=1, max_length=50, examples=["Surname"], default=None)
    ]
    patronymic: Annotated[
        str | None, Field(min_length=1, max_length=40, examples=["Patronymic"], default=None)
    ]

    username_telegram: Annotated[str, Field(min_length=1, max_length=60, examples=["tg_name"])]

    email: Annotated[
        EmailStr | None, Field(examples=["customer.customer@example.com"], default=None)
    ]


class Customer(TimestampSchema, CustomerBase, UUIDSchema, PersistentDeletion):
    tier_id: int | None = None


class CustomerRead(CustomerBase):
    tier_id: int | None = None


class CustomerCreate(CustomerBase):
    model_config = ConfigDict(extra="forbid")


class CustomerCreateInternal(CustomerCreate):
    pass


class CustomerUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Annotated[
        str | None, Field(min_length=1, max_length=30, examples=["Name"], default=None)
    ]
    surname: Annotated[
        str | None, Field(min_length=1, max_length=50, examples=["Surname"], default=None)
    ]
    patronymic: Annotated[
        str | None, Field(min_length=1, max_length=40, examples=["Patronymic"], default=None)
    ]

    username_telegram: Annotated[
        str | None, Field(min_length=1, max_length=60, examples=["tg_name"], default=None)
    ]

    email: Annotated[
        EmailStr | None, Field(examples=["customer.customer@example.com"], default=None)
    ]


class CustomerUpdateInternal(CustomerUpdate):
    updated_at: datetime


class CustomerTierUpdate(BaseModel):
    tier_id: int | None = None


class CustomerDelete(BaseModel):
    model_config = ConfigDict(extra="forbid")

    is_deleted: bool
    deleted_at: datetime


class CustomerRestoreDeleted(BaseModel):
    is_deleted: bool
