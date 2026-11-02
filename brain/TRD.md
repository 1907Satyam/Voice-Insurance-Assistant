# Technical Requirements Document (TRD): Voice-First Vernacular Insurance Assistant

## 1. System Architecture Overview
The application follows a decoupled client-server architecture:
* **Frontend:** React + Vite single-page application communicating via REST APIs and WebSocket/FormData uploads.
* **Backend:** Python FastAPI asynchronous web server managing business logic, database queries, and third-party AI orchestrations.
* **AI Layer:** Gnani AI APIs (**Prisma** for STT, **Evon** for LLM reasoning/intent, **Timbre** for TTS).

## 2. External API Specifications (Gnani AI)
* **Prisma (Speech-to-Text):**
  * Endpoint: `POST /v1/stt` (or provider-specific endpoint)
  * Input: Multipart form-data containing `.wav` / `.webm` audio chunk.
  * Output: Clean transcribed text string in Hindi/Hinglish/English.
* **Evon (LLM / Reasoning Engine):**
  * Endpoint: `POST /v1/chat/completions` (OpenAI-compatible wrapper or Gnani native SDK)
  * Input: System prompt with context, user transcript, and retrieved policy snippets.
  * Output: Structured JSON containing intent, response text, and action flags.
* **Timbre (Text-to-Speech):**
  * Endpoint: `POST /v1/tts`
  * Input: Plain text response string + voice profile/language config.
  * Output: Audio stream (`.mp3` or `.wav`) for browser playback.

## 3. Backend Technical Stack
* **Framework:** FastAPI (`uvicorn` ASGI server)
* **ORM:** SQLAlchemy with SQLite (local development) / PostgreSQL (production)
* **Validation:** Pydantic v2 for request/response schemas
* **Environment Management:** `python-dotenv` for secure API key handling

## 4. Frontend Technical Stack
* **Library:** React 18+ with Vite bundler
* **Styling:** Tailwind CSS for responsive, mobile-first design
* **Audio Handling:** Native browser `MediaRecorder` API recording audio blobs, HTML5 `Audio` element for playback.