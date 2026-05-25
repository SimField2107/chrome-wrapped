import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import runs
from app.services.cleanup import cleanup_expired_runs


@asynccontextmanager
async def lifespan(app: FastAPI):
    cleanup_task = asyncio.create_task(periodic_cleanup())
    yield
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


async def periodic_cleanup():
    """Run cleanup every hour."""
    while True:
        try:
            count = cleanup_expired_runs()
            if count > 0:
                print(f"Cleaned up {count} expired runs")
        except Exception as e:
            print(f"Cleanup error: {e}")
        await asyncio.sleep(3600)


app = FastAPI(
    title="Chrome Wrapped API",
    description="Transform your browsing history into beautiful insights",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "chrome-extension://*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(runs.router, prefix="/runs", tags=["runs"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
