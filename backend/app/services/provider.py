from app.config import settings


class ProviderConfigurationError(RuntimeError):
    pass


def provider_headers() -> dict[str, str]:
    if not settings.gnani_api_key_id:
        raise ProviderConfigurationError("GNANI_API_KEY_ID is not configured.")
    return {"X-API-Key-ID": settings.gnani_api_key_id}


def require_endpoint(endpoint: str, name: str) -> str:
    if not endpoint:
        raise ProviderConfigurationError(f"{name} is not configured.")
    return endpoint
