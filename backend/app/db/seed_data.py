from app.db.database import Base, SessionLocal, engine
from app.db.models import Claim, Policy, User


def seed_data() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.query(Policy).first():
            return

        user = User(name="Demo User", phone="9999999999", preferred_language="hi")
        db.add(user)
        db.flush()
        policies = [
            Policy(
                policy_number="MOTOR-2026-1042",
                user_id=user.id,
                type="motor",
                name="Suraksha Motor Comprehensive",
                insurer="Bharat Suraksha Insurance",
                premium_inr=8420,
                sum_insured_inr=650000,
                start_date="2026-01-01",
                end_date="2026-12-31",
                coverage=[
                    "Accidental damage to the insured vehicle",
                    "Third-party property damage and bodily injury",
                    "Fire, theft, flood, and other listed natural calamities",
                    "Towing assistance up to INR 2,000",
                ],
                exclusions=[
                    "Normal wear and tear or mechanical breakdown",
                    "Driving without a valid licence",
                    "Driving under the influence of alcohol or drugs",
                ],
                description="Comprehensive private car insurance with own-damage and third-party cover.",
            ),
            Policy(
                policy_number="HEALTH-2026-2088",
                user_id=user.id,
                type="health",
                name="Parivaar Health Plus",
                insurer="Bharat Suraksha Insurance",
                premium_inr=12600,
                sum_insured_inr=500000,
                start_date="2026-04-01",
                end_date="2027-03-31",
                coverage=[
                    "In-patient hospitalisation above 24 hours",
                    "Emergency ambulance up to INR 2,000 per hospitalisation",
                    "Pre- and post-hospitalisation expenses for 30 and 60 days",
                    "Cashless treatment at network hospitals, subject to approval",
                ],
                exclusions=[
                    "Non-medical personal comfort items",
                    "Treatments listed in the policy waiting-period clause",
                    "Expenses without required medical records or bills",
                ],
                description="Family floater health cover; waiting periods and sub-limits apply.",
            ),
        ]
        db.add_all(policies)
        db.add(
            Claim(
                reference_id="CLM-9842",
                user_id=user.id,
                policy_id=None,
                incident_type="motor",
                incident_date="2026-10-28",
                incident_location="Jaipur",
                description="Demo claim for a damaged car bumper.",
                status="UNDER_REVIEW",
                status_message="Documents received. An assessor is reviewing the claim.",
            )
        )
        db.commit()
