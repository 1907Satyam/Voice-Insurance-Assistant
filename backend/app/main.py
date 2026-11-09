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

# Parse CORS origins whether passed as a comma-separated string or a list,
# strip trailing slashes, and fall back safely to wildcard if unset.
raw_origins = getattr(settings, "cors_origins", "*")
if isinstance(raw_origins, str):
    origins = [o.strip().rstrip("/") for o in raw_origins.split(",") if o.strip()]
else:
    origins = [str(o).rstrip("/") for o in raw_origins] if raw_origins else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(voice.router, prefix="/api/v1")
app.include_router(policies.router, prefix="/api/v1")
app.include_router(claims.router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}