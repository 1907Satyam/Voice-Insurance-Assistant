import re
from collections.abc import Sequence

from app.db.models import Claim, Policy

CATEGORY_TERMS = {
    "health": {
        "health", "medical", "hospital", "ambulance", "mediclaim", "treatment",
        "हेल्थ", "स्वास्थ्य", "अस्पताल", "दवा", "इलाज", "डॉक्टर", "चिकित्सा", "एम्बुलेंस",
    },
    "motor": {
        "motor", "car", "vehicle", "gaadi", "bike", "bumper", "accident", "गाड़ी",
        "कार", "बाइक", "दुर्घटना", "मोटर",
    },
}


def retrieve_policies(query: str, policies: Sequence[Policy], limit: int = 4) -> list[Policy]:
    terms = set(re.findall(r"[\w]+", query.lower()))
    if not terms:
        return list(policies[:limit])

    def score(policy: Policy) -> int:
        searchable = " ".join(
            [policy.name, policy.type, policy.description, *(policy.coverage or []), *(policy.exclusions or [])]
        ).lower()
        text_score = sum(1 for term in terms if term in searchable)
        category_score = 3 * sum(
            1 for term in terms & CATEGORY_TERMS.get(policy.type, set())
        )
        return text_score + category_score

    ranked = sorted(policies, key=score, reverse=True)
    return [policy for policy in ranked[:limit] if score(policy) > 0] or list(policies[:limit])


def policy_context(policies: Sequence[Policy]) -> list[dict]:
    return [
        {
            "policy_number": policy.policy_number,
            "type": policy.type,
            "name": policy.name,
            "insurer": policy.insurer,
            "sum_insured_inr": policy.sum_insured_inr,
            "coverage": policy.coverage,
            "exclusions": policy.exclusions,
            "description": policy.description,
        }
        for policy in policies
    ]


def claim_context(claims: Sequence[Claim]) -> list[dict]:
    return [
        {
            "reference_id": claim.reference_id,
            "incident_type": claim.incident_type,
            "status": claim.status,
            "status_message": claim.status_message,
            "incident_date": claim.incident_date,
        }
        for claim in claims
    ]
