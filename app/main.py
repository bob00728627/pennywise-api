from fastapi import FastAPI

from app.core.config import get_settings

config = get_settings()
app = FastAPI(title=config.app_name, version="0.1.0")


@app.get("/api/health", tags=["meta"])
def health() -> dict[str, str]:
    return {"status": "ok", "version": app.version}
