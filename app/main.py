"""API FastAPI — ARANDU."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import dashboard, filtros
from app.config import settings
from app.database import check_connection

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("arandu.api")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifecycle da aplicação."""
    logger.info("ARANDU API iniciada — cobertura nacional")
    yield
    logger.info("ARANDU API encerrada")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="API de Monitoramento e Inteligência Territorial — Brasil",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(filtros.router, prefix="/api/v1")


@app.get("/health")
def health() -> dict[str, str]:
    """Health check com status do banco."""
    db_ok = check_connection()
    return {
        "status": "ok" if db_ok or settings.use_mock_data else "degraded",
        "app": settings.app_name,
        "version": settings.version,
        "database": "connected" if db_ok else "unavailable",
        "data_source": "mock" if settings.use_mock_data else "database",
    }


@app.exception_handler(Exception)
async def global_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    """Tratamento global de erros."""
    logger.exception("Erro não tratado: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Erro interno do servidor"})
