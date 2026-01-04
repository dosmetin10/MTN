from fastapi import APIRouter

from app.api.v1 import health, stock, customers

router = APIRouter()
router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(customers.router, prefix="/customers", tags=["customers"])
router.include_router(stock.router, prefix="/stock", tags=["stock"])
