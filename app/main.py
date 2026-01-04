from fastapi import FastAPI

from app.api.router import api_router
from app.core.database import init_db
from app.core.settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name, version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    init_db()


app.include_router(api_router)
