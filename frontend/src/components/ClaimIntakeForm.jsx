import { useState } from "react";
import { createClaim, uploadClaimDocuments } from "../services/api.js";
import DocumentUploader from "./DocumentUploader.jsx";

export default function ClaimIntakeForm({ policies, onCreated }) {
  const [incidentType, setIncidentType] = useState("motor");
  const [policyNumber, setPolicyNumber] = useState("");
  const [incidentDate, setIncidentDate] = useState("");
  const [location, setLocation] = useState("");
  const [description, setDescription] = useState("");
  const [files, setFiles] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const matchingPolicies = policies.filter((policy) => policy.type === incidentType);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const claim = await createClaim({
        incident_type: incidentType,
        policy_number: policyNumber || null,
        incident_date: incidentDate || null,
        incident_location: location || null,
        description,
      });
      if (files.length) {
        try {
          await uploadClaimDocuments(claim.reference_id, files);
        } catch (cause) {
          onCreated(
            { ...claim, incident_type: incidentType },
            `Claim ${claim.reference_id} is registered, but document upload failed: ${cause.message}`,
          );
          return;
        }
      }
      onCreated({
        reference_id: claim.reference_id,
        status: claim.status,
        status_message: files.length
          ? `${claim.status_message} ${files.length} document(s) attached.`
          : claim.status_message,
        incident_type: incidentType,
      });
    } catch (cause) {
      setError(cause.message || "Claim submit नहीं हुआ। कृपया फिर से कोशिश करें।");
    } finally {
      setBusy(false);
    }
  }

  return (
    <form className="claim-intake" onSubmit={submit}>
      <p className="eyebrow">CLAIM DETAILS</p>
      <h3>थोड़ी जानकारी साझा करें</h3>
      <label>Claim type
        <select value={incidentType} onChange={(event) => { setIncidentType(event.target.value); setPolicyNumber(""); }}>
          <option value="motor">Motor / गाड़ी</option>
          <option value="health">Health / स्वास्थ्य</option>
        </select>
      </label>
      <label>Policy
        <select value={policyNumber} onChange={(event) => setPolicyNumber(event.target.value)}>
          <option value="">Select a policy (optional)</option>
          {matchingPolicies.map((policy) => <option value={policy.policy_number} key={policy.policy_number}>{policy.name}</option>)}
        </select>
      </label>
      <div className="claim-form-row">
        <label>Incident date
          <input type="date" value={incidentDate} onChange={(event) => setIncidentDate(event.target.value)} />
        </label>
        <label>Location
          <input value={location} onChange={(event) => setLocation(event.target.value)} placeholder="City / area" />
        </label>
      </div>
      <label>What happened?
        <textarea required minLength={5} maxLength={4000} value={description} onChange={(event) => setDescription(event.target.value)} placeholder="Describe the incident in a few words" />
      </label>
      <DocumentUploader files={files} onFiles={setFiles} />
      <button className="claim-submit" type="submit" disabled={busy}>
        {busy ? "Submitting…" : "Submit claim details"}
      </button>
      {error && <p className="claim-form-error" role="alert">{error}</p>}
      <p className="claim-form-note">Submitting starts a claim record. The insurer will verify eligibility and documents.</p>
    </form>
  );
}
