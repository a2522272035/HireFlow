from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import interview, policy, report, resume, wecom
from app.config import settings
from app.core.database import engine
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="智能招聘面试辅助系统",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，解决跨域问题
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": settings.APP_NAME}


# API v1 routes
app.include_router(resume.router, prefix="/api/v1/resumes", tags=["resumes"])
app.include_router(interview.router, prefix="/api/v1/interviews", tags=["interviews"])
app.include_router(report.router, prefix="/api/v1/reports", tags=["reports"])
app.include_router(policy.router, prefix="/api/v1/policies", tags=["policies"])
app.include_router(wecom.router, prefix="/api/v1/wecom", tags=["wecom"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8002)
