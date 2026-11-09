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

vercel_origin = "https://voice-insurance-assistant.vercel.app"
origins = list(
    dict.fromkeys(
        origin.rstrip("/")
        for origin in [*settings.cors_origins, vercel_origin]
        if origin.strip()
    )
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(voice.router, prefix="/api/v1")
app.include_router(policies.router, prefix="/api/v1")
app.include_router(claims.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}