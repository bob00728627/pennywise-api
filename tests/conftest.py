import os
import tempfile

import pytest

_db_dir = tempfile.mkdtemp()
os.environ["PENNYWISE_DATABASE_URL"] = f"sqlite:///{_db_dir}/test.db"
os.environ["PENNYWISE_SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient  # noqa: E402

from app.database import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as c:
        yield c


def register(client: TestClient, email: str = "alex@example.com", demo: bool = False) -> dict[str, str]:
    res = client.post("/api/auth/register",
                      json={"email": email, "name": "Alex", "password": "supersecret", "seedDemo": demo})
    assert res.status_code == 201, res.text
    return {"Authorization": f"Bearer {res.json()['accessToken']}"}


@pytest.fixture
def auth(client: TestClient) -> dict[str, str]:
    return register(client)


@pytest.fixture
def demo_auth(client: TestClient) -> dict[str, str]:
    return register(client, "demo@example.com", demo=True)
