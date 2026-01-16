from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import config, scans, test_api

# In-memory storage for MVP (replace with database later)
scan_storage: dict[str, dict] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="PromptShield API",
    description="REST API for LLM Security Gate",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scans.router, prefix="/api/v1", tags=["scans"])
app.include_router(test_api.router, prefix="/api/v1", tags=["test-api"])
app.include_router(config.router, prefix="/api/v1", tags=["config"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "promptshield-api"}


@app.get("/")
async def root():
    return {
        "service": "PromptShield API",
        "version": "1.0.0",
        "docs": "/docs",
    }

