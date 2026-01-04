from fastapi import APIRouter

from app.schemas.system import HealthResponse

router = APIRouter()


@router.get("", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return HealthResponse(status="ok")
