# Application Flow & Sequence: Voice Insurance Assistant

## 1. High-Level User Journey
## 2. Detailed Step-by-Step Sequence
1. **Initiation:** User opens the React web app on mobile or desktop and taps the glowing microphone button (`VoiceRecorder.jsx`).
2. **Audio Capture:** The browser captures mic input until the user taps stop or silence is detected. The file is packaged as a `.webm` or `.wav` blob.
3. **Upload to FastAPI:** Frontend sends a `POST /api/v1/voice/interact` request with the audio file form-data.
4. **Speech-to-Text (Prisma):** FastAPI service calls `prisma_stt.py` to convert audio bytes into text (e.g., *"Gaadi ka bumper toot gaya, claim kaise bharein?"*).
5. **Intent Parsing & RAG (Evon):** 
   * `evon_llm.py` analyzes the transcript.
   * Matches intent to either `CHECK_COVERAGE`, `FILE_CLAIM`, or `CLAIM_STATUS`.
   * Queries local policy database or vector index (`rag_engine.py`) if policy clauses are needed.
6. **Text Generation:** Evon formulates a concise, natural response in Hinglish.
7. **Text-to-Speech (Timbre):** `timbre_tts.py` converts the textual response into audio bytes.
8. **Client Response:** FastAPI returns a JSON payload containing the user transcript, bot text response, and audio stream URL/base64 audio.
9. **UI Render & Playback:** Frontend displays the chat bubbles (`ChatBubble.jsx`), renders any relevant UI cards (`PolicyCard.jsx` or `ClaimStatusBadge.jsx`), and auto-plays the voice response.

## 3. Claim Intake and Supporting Documents
1. When Evon identifies `FILE_CLAIM`, the client renders a claim intake form for
   the incident type, policy, date, location, and description.
2. The client submits the completed details to `POST /api/v1/claims`; the API
   returns a claim reference and initial status.
3. Optional PDF/JPEG/PNG/WebP evidence is uploaded to
   `POST /api/v1/claims/{reference_id}/documents`. Each file is size-limited,
   type-checked, stored under `UPLOAD_DIR`, and linked to the claim.
4. `GET /api/v1/claims/{reference_id}` returns status and attached document
   metadata. Authenticated document access must be added before production use.

## 4. Text Prompt and Data APIs
The example prompt chips use `POST /api/v1/voice/interact/text`, which skips
Prisma STT and runs the same Evon → Timbre response path. `GET
/api/v1/policies` supplies the policy options used in the claim intake form.