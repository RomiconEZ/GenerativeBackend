from fastapi import APIRouter

from .customer import router as customer_router
from .review import router as review_router
from .tour import router as tour_router
from .waiting_cutomer import router as waiting_cutomer_router
from .agent import router as agent_router

router = APIRouter(prefix="/v1")

router.include_router(customer_router)
router.include_router(waiting_cutomer_router)
router.include_router(review_router)
router.include_router(tour_router)
router.include_router(agent_router)
