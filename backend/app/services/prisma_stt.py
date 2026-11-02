import httpx

from app.config import settings
from app.services.provider import provider_headers, require_endpoint


async def transcribe_audio(audio: bytes, filename: str, content_type: str) -> str:
    endpoint = require_endpoint(settings.prisma_stt_url, "PRISMA_STT_URL")
    headers = provider_headers()
    async with httpx.AsyncClient(timeout=httpx.Timeout(90.0)) as client:
        response = await client.post(
            endpoint,
            headers=headers,
            files={"file": (filename, audio, content_type or "application/octet-stream")},
        )
        response.raise_for_status()
    try:
        payload = response.json()
    except ValueError as exc:
        raise ValueError("Prisma STT returned an invalid JSON response.") from exc
    transcript = payload.get("text") or payload.get("transcript")
    if not transcript and isinstance(payload.get("data"), dict):
        transcript = payload["data"].get("text") or payload["data"].get("transcript")
    if not isinstance(transcript, str) or not transcript.strip():
        raise ValueError("Prisma STT response did not contain transcript text.")
    return transcript.strip()
