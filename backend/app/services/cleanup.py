"""
Cleanup service for expired Wrapped runs.
"""

from datetime import UTC, datetime

from sqlmodel import Session, select

from app.models.db import WrappedRun, engine


def cleanup_expired_runs() -> int:
    """
    Delete all expired Wrapped runs.
    Returns the number of runs deleted.
    """
    with Session(engine) as session:
        now = datetime.now(UTC)
        statement = select(WrappedRun).where(
            WrappedRun.expires_at.isnot(None),
            WrappedRun.expires_at < now,
        )
        expired_runs = session.exec(statement).all()

        count = len(expired_runs)
        for run in expired_runs:
            session.delete(run)

        session.commit()
        return count
