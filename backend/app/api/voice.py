import logging
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
import httpx
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import get_db
from app.db.models import Claim, Policy
from app.services.evon_llm import understand_query
from app.services.prisma_stt import transcribe_audio
from app.services.provider import ProviderConfigurationError
from app.services.rag_engine import claim_context, policy_context, retrieve_policies
from app.services.timbre_tts import synthesize_speech

router = APIRouter(prefix="/voice", tags=["voice"])
logger = logging.getLogger(__name__)


class TextInteraction(BaseModel):
    text: str = Field(min_length=1, max_length=4000)


def _http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, ProviderConfigurationError):
        return HTTPException(status_code=503, detail=str(exc))
    if isinstance(exc, httpx.HTTPStatusError):
        return HTTPException(
            status_code=502,
            detail=f"AI provider request failed (HTTP {exc.response.status_code}).",
        )
    if isinstance(exc, httpx.TimeoutException):
        return HTTPException(status_code=504, detail="AI provider request timed out.")
    if isinstance(exc, httpx.RequestError):
        return HTTPException(status_code=502, detail="Could not connect to the AI provider.")
    if isinstance(exc, ValueError):
        return HTTPException(status_code=502, detail="AI provider returned an invalid response.")
    logger.error(
        "Unexpected AI provider integration error",
        exc_info=(type(exc), exc, exc.__traceback__),
    )
    return HTTPException(status_code=502, detail="AI provider could not process this request.")


async def _build_response(transcript: str, db: Session) -> dict:
    all_policies = db.query(Policy).all()
    relevant_policies = retrieve_policies(transcript, all_policies)
    claims = db.query(Claim).order_by(Claim.created_at.desc()).limit(20).all()
    try:
        result = await understand_query(
            transcript, policy_context(relevant_policies), claim_context(claims)
        )
        audio_base64, audio_content_type = await synthesize_speech(result["response"])
    except Exception as exc:
        raise _http_error(exc) from exc

    policy = next(
        (item for item in relevant_policies if item.policy_number == result.get("policy_number")),
        relevant_policies[0] if result["intent"] == "CHECK_COVERAGE" and relevant_policies else None,
    )
    claim = next(
        (item for item in claims if item.reference_id == result.get("claim_reference")),
        None,
    )
    return {
        "transcript": transcript,
        "response": result["response"],
        "intent": result["intent"],
        "audio_base64": audio_base64,
        "audio_content_type": audio_content_type,
        "policy": {
            "policy_number": policy.policy_number,
            "type": policy.type,
            "name": policy.name,
            "insurer": policy.insurer,
            "sum_insured_inr": policy.sum_insured_inr,
            "coverage": policy.coverage,
            "exclusions": policy.exclusions,
        }
        if policy
        else None,
        "claim": {
            "reference_id": claim.reference_id,
            "status": claim.status,
            "status_message": claim.status_message,
            "incident_type": claim.incident_type,
        }
        if claim
        else None,
    }


@router.post("/interact")
async def interact(
    audio: UploadFile = File(...),
    language: str = Form(default="hi"),
    db: Session = Depends(get_db),
):
    max_bytes = settings.max_audio_size_mb * 1024 * 1024
    audio_bytes = await audio.read(max_bytes + 1)
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Audio recording is empty.")
    if len(audio_bytes) > max_bytes:
        raise HTTPException(status_code=413, detail="Audio recording exceeds the upload limit.")
    if audio.content_type and not (
        audio.content_type.startswith("audio/") or audio.content_type == "application/octet-stream"
    ):
        raise HTTPException(status_code=415, detail="Upload must be an audio recording.")
    try:
        transcript = await transcribe_audio(
            audio_bytes,
            audio.filename or f"recording-{uuid4().hex}.webm",
            audio.content_type or "application/octet-stream",
        )
    except Exception as exc:
        raise _http_error(exc) from exc
    result = await _build_response(transcript, db)
    result["language"] = language
    return result


@router.post("/interact/text")
async def interact_with_text(payload: TextInteraction, db: Session = Depends(get_db)):
    return await _build_response(payload.text.strip(), db)
