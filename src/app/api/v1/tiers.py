from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_superagent
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import DuplicateValueException, NotFoundException
from ...crud.crud_tier import crud_tiers
from ...schemas.tier import TierCreate, TierCreateInternal, TierRead, TierUpdate

router = APIRouter(tags=["tiers"])


@router.post("/tier", status_code=201)
async def write_tier(
    request: Request, self_agent_id: int, tier: TierCreate, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> TierRead:
    await get_current_superagent(self_agent_id, db)

    tier_internal_dict = tier.model_dump()
    db_tier = await crud_tiers.exists(db=db, name=tier_internal_dict["name"])
    if db_tier:
        raise DuplicateValueException("Tier Name not available")

    tier_internal = TierCreateInternal(**tier_internal_dict)
    created_tier: TierRead = await crud_tiers.create(db=db, object=tier_internal)
    return created_tier


@router.get("/tiers", response_model=PaginatedListResponse[TierRead])
async def read_tiers(
    request: Request, db: Annotated[AsyncSession, Depends(async_get_db)], page: int = 1, items_per_page: int = 10
) -> dict:
    tiers_data = await crud_tiers.get_multi(
        db=db, offset=compute_offset(page, items_per_page), limit=items_per_page, schema_to_select=TierRead
    )

    response: dict[str, Any] = paginated_response(crud_data=tiers_data, page=page, items_per_page=items_per_page)
    return response


@router.get("/tier/{name}", response_model=TierRead)
async def read_tier(request: Request, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict:
    db_tier: TierRead | None = await crud_tiers.get(db=db, schema_to_select=TierRead, name=name)
    if db_tier is None:
        raise NotFoundException("Tier not found")

    return db_tier


@router.patch("/tier/{name}")
async def patch_tier(
    request: Request, agent_id: int, values: TierUpdate, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]
) -> dict[str, str]:
    await get_current_superagent(agent_id, db)
    db_tier = await crud_tiers.get(db=db, schema_to_select=TierRead, name=name)
    if db_tier is None:
        raise NotFoundException("Tier not found")

    await crud_tiers.update(db=db, object=values, name=name)
    return {"message": "Tier updated"}


@router.delete("/tier/{name}")
async def erase_tier(request: Request, agent_id: int, name: str, db: Annotated[AsyncSession, Depends(async_get_db)]) -> dict[str, str]:
    await get_current_superagent(agent_id, db)

    db_tier = await crud_tiers.get(db=db, schema_to_select=TierRead, name=name)
    if db_tier is None:
        raise NotFoundException("Tier not found")

    await crud_tiers.delete(db=db, name=name)
    return {"message": "Tier deleted"}
