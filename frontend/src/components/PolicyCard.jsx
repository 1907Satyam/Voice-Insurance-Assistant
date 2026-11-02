import { ShieldCheck, IndianRupee } from "lucide-react";

const formatRupees = (value) => new Intl.NumberFormat("en-IN", { maximumFractionDigits: 0 }).format(value);

export default function PolicyCard({ policy }) {
  return (
    <section className="data-card policy-card">
      <div className="card-title-row">
        <div className="card-icon"><ShieldCheck size={18} /></div>
        <div><p className="eyebrow">{policy.type} policy</p><h3>{policy.name}</h3></div>
      </div>
      <div className="policy-sum"><IndianRupee size={16} /> {formatRupees(policy.sum_insured_inr)} <span>sum insured</span></div>
      <p className="policy-meta">{policy.insurer} <span>·</span> {policy.policy_number}</p>
      {policy.coverage?.length > 0 && (
        <div className="coverage-list">
          <p className="eyebrow">Relevant benefits</p>
          {policy.coverage.slice(0, 3).map((item) => <div className="coverage-item" key={item}><span />{item}</div>)}
        </div>
      )}
      <p className="fine-print">Final cover is subject to policy terms, limits and exclusions.</p>
    </section>
  );
}
