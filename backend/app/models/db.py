import json
from datetime import UTC, datetime
from typing import Any

from sqlmodel import Field, Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./chrome_wrapped.db"
engine = create_engine(DATABASE_URL, echo=False)


class WrappedRun(SQLModel, table=True):
    __tablename__ = "wrapped_runs"

    id: str = Field(primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    timezone: str
    range_start: str
    range_end: str
    raw_history: str
    insights_json: str | None = None
    expires_at: datetime | None = None

    def set_history(self, history: list[dict[str, Any]]) -> None:
        self.raw_history = json.dumps(history)

    def get_history(self) -> list[dict[str, Any]]:
        return json.loads(self.raw_history)

    def set_insights(self, insights: dict[str, Any]) -> None:
        self.insights_json = json.dumps(insights)

    def get_insights(self) -> dict[str, Any] | None:
        if self.insights_json:
            return json.loads(self.insights_json)
        return None


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
