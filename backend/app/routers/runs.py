import uuid
from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.models.db import WrappedRun, get_session, init_db
from app.models.schemas import CreateRunRequest, CreateRunResponse, Insights
from app.services.analytics import compute_insights

router = APIRouter()

init_db()


@router.post("", response_model=CreateRunResponse)
async def create_run(
    request: CreateRunRequest,
    session: Session = Depends(get_session),
) -> CreateRunResponse:
    run_id = str(uuid.uuid4())

    run = WrappedRun(
        id=run_id,
        timezone=request.timezone,
        range_start=request.range_start,
        range_end=request.range_end,
        raw_history="[]",
        expires_at=datetime.now(UTC) + timedelta(hours=24),
    )
    run.set_history([item.model_dump() for item in request.history])

    insights = compute_insights(
        history=[item.model_dump() for item in request.history],
        run_id=run_id,
        timezone=request.timezone,
        range_start=request.range_start,
        range_end=request.range_end,
    )
    run.set_insights(insights.model_dump(by_alias=True))

    session.add(run)
    session.commit()

    return CreateRunResponse(run_id=run_id)


@router.get("/{run_id}/insights", response_model=Insights)
async def get_insights(
    run_id: str,
    session: Session = Depends(get_session),
) -> Insights:
    run = session.get(WrappedRun, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    insights_data = run.get_insights()
    if not insights_data:
        raise HTTPException(status_code=404, detail="Insights not ready")

    return Insights.model_validate(insights_data)
