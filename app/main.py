from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401  (register tables)
from app.core.config import get_settings
from app.database import Base, engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


config = get_settings()
app = FastAPI(title=config.app_name, version="0.1.0", lifespan=lifespan)


@app.get("/api/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok", "version": app.version}
