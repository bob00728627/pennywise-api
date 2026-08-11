import os
import tempfile

import pytest

_db_dir = tempfile.mkdtemp()
os.environ["PENNYWISE_DATABASE_URL"] = f"sqlite:///{_db_dir}/test.db"
os.environ["PENNYWISE_SECRET_KEY"] = "test-secret"

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


@pytest.fixture
def client() -> TestClient:
    with TestClient(app) as c:
        yield c
