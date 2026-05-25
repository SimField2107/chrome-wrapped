import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.models.db import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_history():
    return [
        {
            "url": "https://www.google.com/search?q=test",
            "title": "test - Google Search",
            "visitCount": 10,
            "visits": [
                {"timestamp": 1704067200000, "transition": "link"},
                {"timestamp": 1704153600000, "transition": "typed"},
            ],
        },
        {
            "url": "https://github.com/user/repo",
            "title": "user/repo - GitHub",
            "visitCount": 5,
            "visits": [
                {"timestamp": 1704240000000, "transition": "link"},
            ],
        },
        {
            "url": "https://www.youtube.com/watch?v=abc123",
            "title": "Cool Video - YouTube",
            "visitCount": 3,
            "visits": [
                {"timestamp": 1704326400000, "transition": "link"},
                {"timestamp": 1704412800000, "transition": "link"},
                {"timestamp": 1704499200000, "transition": "link"},
            ],
        },
    ]
