from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Policy

router = APIRouter(tags=["policies"])


@router.get("/api/v1/policies")
@router.get("/api/policies", include_in_schema=False)
def list_policies(db: Session = Depends(get_db)):
    policies = db.query(Policy).order_by(Policy.id).all()
    return [
        {
            "policy_number": policy.policy_number,
            "type": policy.type,
            "name": policy.name,
            "insurer": policy.insurer,
            "premium_inr": policy.premium_inr,
            "sum_insured_inr": policy.sum_insured_inr,
            "start_date": policy.start_date,
            "end_date": policy.end_date,
            "coverage": policy.coverage,
            "exclusions": policy.exclusions,
        }
        for policy in policies
    ]
