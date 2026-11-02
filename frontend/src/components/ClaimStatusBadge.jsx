import { ClipboardCheck } from "lucide-react";

const STATUS_LABELS = {
  SUBMITTED: "दर्ज · Submitted",
  UNDER_REVIEW: "जाँच जारी · Under review",
  NEEDS_INFORMATION: "जानकारी चाहिए · Needs information",
  APPROVED: "स्वीकृत · Approved",
  REJECTED: "अस्वीकृत · Rejected",
  SETTLED: "भुगतान पूरा · Settled",
};

export default function ClaimStatusBadge({ claim }) {
  return (
    <section className="data-card claim-card">
      <div className="claim-top">
        <div className="card-icon"><ClipboardCheck size={18} /></div>
        <div><p className="eyebrow">Claim reference</p><h3>{claim.reference_id}</h3></div>
        <span className={`status-pill status-${claim.status?.toLowerCase()}`}>{STATUS_LABELS[claim.status] || claim.status}</span>
      </div>
      <p className="claim-note">{claim.status_message || "आपके claim की जानकारी यहाँ दिखाई देगी।"}</p>
    </section>
  );
}
