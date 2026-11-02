from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import claims, policies, voice
from app.config import settings
from app.db.seed_data import seed_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    seed_data()
    yield


app = FastAPI(
    title=settings.project_name,
    description="Hindi and Hinglish voice support for insurance policies and claims.",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
app.include_router(voice.router)
app.include_router(policies.router)
app.include_router(claims.router)


@app.get("/health")
def health():
    return {"status": "ok"}
