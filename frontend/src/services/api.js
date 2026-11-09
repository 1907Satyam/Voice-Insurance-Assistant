const API_BASE_URL = import.meta.env.VITE_API_BASE_URL?.trim().replace(/\/+$/, "");

function apiUrl(path) {
  if (!API_BASE_URL) {
    throw new Error("VITE_API_BASE_URL is not configured for this deployment.");
  }
  return `${API_BASE_URL}/api/v1/${path.replace(/^\/+/, "")}`;
}

async function readResponse(response) {
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      message = body.detail || message;
    } catch {
      // Keep the HTTP status message when the server does not return JSON.
    }
    throw new Error(message);
  }
  return response.json();
}

export async function sendAudio(audioBlob) {
  const formData = new FormData();
  formData.append("audio", audioBlob, `recording.${audioBlob.type.includes("ogg") ? "ogg" : "webm"}`);
  formData.append("language", "hi");
  return readResponse(
    await fetch(apiUrl("voice/interact"), { method: "POST", body: formData }),
  );
}

export async function sendText(text) {
  return readResponse(
    await fetch(apiUrl("voice/interact/text"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    }),
  );
}

export async function fetchPolicies() {
  return readResponse(await fetch(apiUrl("policies")));
}

export async function createClaim(claim) {
  return readResponse(
    await fetch(apiUrl("claims"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(claim),
    }),
  );
}

export async function uploadClaimDocuments(referenceId, files) {
  const formData = new FormData();
  files.forEach((file) => formData.append("files", file));
  return readResponse(
    await fetch(apiUrl(`claims/${encodeURIComponent(referenceId)}/documents`), {
      method: "POST",
      body: formData,
    }),
  );
}
