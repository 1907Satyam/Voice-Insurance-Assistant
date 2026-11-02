import base64

import httpx

from app.config import settings
from app.services.provider import provider_headers, require_endpoint


async def synthesize_speech(text: str, language: str = "hi") -> tuple[str, str]:
    endpoint = require_endpoint(settings.timbre_tts_url, "TIMBRE_TTS_URL")
    body = {
        "text": text,
        "voice": settings.timbre_voice,
        "model": settings.timbre_model,
        "language": language,
    }
    async with httpx.AsyncClient(timeout=httpx.Timeout(90.0)) as client:
        response = await client.post(endpoint, headers=provider_headers(), json=body)
        response.raise_for_status()
    content_type = response.headers.get("content-type", "").split(";")[0].strip()
    if content_type.startswith("audio/"):
        return base64.b64encode(response.content).decode("ascii"), content_type

    try:
        payload = response.json()
    except ValueError as exc:
        raise ValueError("Timbre returned an unsupported audio response.") from exc
    audio = payload.get("audio_base64") or payload.get("audio")
    if not isinstance(audio, str) or not audio.strip():
        raise ValueError("Timbre response did not contain audio data.")
    return audio, payload.get("content_type", "audio/mpeg")
