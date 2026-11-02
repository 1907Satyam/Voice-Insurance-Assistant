import json

import httpx

from app.config import settings
from app.services.provider import provider_headers, require_endpoint

ALLOWED_INTENTS = {"CHECK_COVERAGE", "FILE_CLAIM", "CLAIM_STATUS", "GENERAL"}


async def understand_query(
    transcript: str, policies: list[dict], claims: list[dict]
) -> dict:
    endpoint = require_endpoint(settings.evon_llm_url, "EVON_LLM_URL")
    system_prompt = (
        "You are a warm, concise Hindi/Hinglish insurance assistant for Indian customers. "
        "Use only the supplied policy and claim data; never invent coverage or claim status. "
        "If the user asks to file a claim, guide them to provide incident date, location, "
        "and a short description; do not claim a claim was filed. "
        "Return only a JSON object with intent (CHECK_COVERAGE, FILE_CLAIM, CLAIM_STATUS, "
        "or GENERAL), response (plain conversational text), policy_number (string or null), "
        "claim_reference (string or null), and incident_type (motor, health, or null). "
        "Be explicit that coverage is subject to policy terms."
    )
    user_content = json.dumps(
        {
            "transcript": transcript,
            "policies": policies,
            "claims": claims,
        },
        ensure_ascii=False,
    )
    body = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    if settings.evon_model:
        body["model"] = settings.evon_model

    async with httpx.AsyncClient(timeout=httpx.Timeout(60.0)) as client:
        response = await client.post(endpoint, headers=provider_headers(), json=body)
        response.raise_for_status()
    try:
        payload = response.json()
        content = payload["choices"][0]["message"]["content"]
        result = json.loads(content)
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        raise ValueError("Evon returned a response that could not be parsed.") from exc
    if not isinstance(result, dict):
        raise ValueError("Evon response must be a JSON object.")

    intent = result.get("intent")
    text = result.get("response")
    if intent not in ALLOWED_INTENTS or not isinstance(text, str) or not text.strip():
        raise ValueError("Evon response is missing a valid intent or response text.")
    result["response"] = text.strip()
    result["intent"] = intent
    return result
