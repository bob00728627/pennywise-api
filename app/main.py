from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models  # noqa: F401  (register tables)
from app.core.config import get_settings
from app.database import Base, engine
from app.routers import auth, budgets, categories, goals, reports, settings, transactions


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


config = get_settings()
app = FastAPI(title=config.app_name, version="1.0.0", lifespan=lifespan,
              description="REST API for the Pennywise personal finance tracker.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for r in (auth, categories, transactions, budgets, goals, reports, settings):
    app.include_router(r.router)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse("/docs")


@app.get("/api/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok", "version": app.version}
