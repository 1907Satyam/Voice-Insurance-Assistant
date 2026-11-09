# Agent Memory & Task Ledger

> **AGENT DIRECTIVE:** The AI Agent **MUST UPDATE THIS FILE AFTER EVERY PROMPT** where actionable work, architectural modifications, API integration, or code implementation takes place. Log precise details of what was requested, what files were created/modified, actual requirements vs. current implementation status, and next steps.

---

## 1. Project Overview & Target Blueprint
* **Project Name:** Voice-First Vernacular Insurance Claim & Policy Assistant
* **Target Domain:** Tier 2 / Tier 3 Financial Literacy & Vernacular Insurance Accessibility
* **Core Integrations:**
  * **Gnani Prisma:** Speech-to-Text (Code-mixed Hinglish & Vernacular transcription)
  * **Gnani Evon / LLM Layer:** Intent parsing, conversational RAG & reasoning
  * **Gnani Timbre:** Text-to-Speech (Natural Hindi/English speech synthesis)
* **Stack:** React + Vite + Tailwind CSS (Frontend), FastAPI + SQLAlchemy + SQLite (Backend)

---

## 2. Requirements Tracking: Actual vs. Built

### Phase 1: Blueprint & Architecture
| Requirement | Status | Scope / Target File | Notes |
| :--- | :--- | :--- | :--- |
| Product Requirements Document (PRD) | **COMPLETED** | `brain/PRD.md` | Defined core features, target audience, and winning differentiators |
| Technical Requirements Document (TRD) | **COMPLETED** | `brain/TRD.md` | Specified Gnani API integrations (Prisma, Evon, Timbre) and tech stack |
| Application Flow & Sequence Diagram | **COMPLETED** | `brain/app_flow.md` | Sequence flows for mic capture, backend processing, RAG, and TTS audio playback |
| Relational Database Schema Design | **COMPLETED** | `brain/database_schema.md` | Designed `users`, `policies`, and `claims` tables |
| Living Agent Memory & Ledger Setup | **COMPLETED** | `brain/Agent_memory.md` | Updated implementation tracking and execution history |

---

### Phase 2: Backend Architecture & Services *(Completed)*
| Requirement | Status | Target File(s) | Notes |
| :--- | :--- | :--- | :--- |
| FastAPI Application Setup & Config | **COMPLETED** | `backend/app/main.py`, `backend/app/config.py` | FastAPI lifespan, CORS, health route, environment configuration |
| Database Models & Seed Script | **COMPLETED** | `backend/app/db/models.py`, `backend/app/db/seed_data.py` | SQLAlchemy user, policy, claim models and seeded Hindi/Hinglish examples |
| Gnani Prisma STT Integration Service | **COMPLETED** | `backend/app/services/prisma_stt.py` | Async multipart audio handler with transcript validation |
| Gnani Evon LLM Intent & RAG Service | **COMPLETED** | `backend/app/services/evon_llm.py`, `backend/app/services/rag_engine.py` | Policy retrieval and structured intent/response processing |
| Gnani Timbre TTS Service | **COMPLETED** | `backend/app/services/timbre_tts.py` | Async Hindi voice synthesis with base64/audio response parsing |
| Voice Interaction Endpoint | **COMPLETED** | `backend/app/api/voice.py` | Audio and text interaction endpoints return transcript, response, action data, and audio |

---

### Phase 3: Frontend User Interface *(Completed)*
| Requirement | Status | Target File(s) | Notes |
| :--- | :--- | :--- | :--- |
| React + Vite App Boilerplate Setup | **COMPLETED** | `frontend/src/App.jsx`, `frontend/*` | Responsive React SPA with Tailwind and API configuration |
| Custom Audio Recorder Hook | **COMPLETED** | `frontend/src/hooks/useAudioRecorder.js` | MediaRecorder permission, capture, timer and cleanup handling |
| Audio Player Hook | **COMPLETED** | `frontend/src/hooks/useAudioPlayer.js` | Plays base64 Timbre audio responses |
| Voice Recorder UI Component | **COMPLETED** | `frontend/src/components/VoiceRecorder.jsx` | Animated mic button, timer and waveform feedback |
| Chat & Policy Card Components | **COMPLETED** | `frontend/src/components/*` | Message feed, policy summary, claim status, and document selection UI |

### Phase 4: Claims & API Support
| Requirement | Status | Target File(s) | Notes |
| :--- | :--- | :--- | :--- |
| Policy and claim HTTP endpoints | **COMPLETED** | `backend/app/api/policies.py`, `backend/app/api/claims.py` | Policy listing, claim creation/status, validated document upload and download |

### Phase 5: Environment Configuration & Secret Hygiene
| Requirement | Status | Target File(s) | Notes |
| :--- | :--- | :--- | :--- |
| Centralized environment configuration | **COMPLETED** | `backend/app/config.py` | Singleton loaded from backend `.env`, requires project/database/upload settings |
| Local and template environment files | **COMPLETED** | `backend/.env`, `backend/.env.example` | Local provider credentials remain blank placeholders; example is safe to commit |
| Ignore local secrets | **COMPLETED** | `backend/.gitignore`, `.gitignore` | Explicit backend `.env` ignore rule |

---

## 3. Interaction Audit & Execution History

### Prompt 1: Initial System Definition & Blueprint Creation
* **Actions Taken:** 
  * Defined core product architecture leveraging Gnani Prisma (STT), Evon (LLM), and Timbre (TTS).
  * Generated project directory structure.
  * Created true context specification files: `brain/PRD.md`, `brain/TRD.md`, `brain/app_flow.md`, `brain/database_schema.md`.
  * Initialized `brain/agent_memory.md` with requirement tracking tables and instructions for automated self-updates across turns.
* **Files Created:**
  * `brain/PRD.md`
  * `brain/TRD.md`
  * `brain/app_flow.md`
  * `brain/database_schema.md`
  * `brain/agent_memory.md`
* **Current Status:** Foundation & design blueprint complete. Ready for implementation.

### Prompt 2: Full-stack voice insurance assistant implementation
* **Actions Taken:**
  * Implemented FastAPI configuration, SQLite/PostgreSQL-compatible SQLAlchemy models, seeded Hindi/Hinglish policies, and policy/claim APIs.
  * Added configurable Gnani Prisma, Evon, and Timbre HTTP integrations, Hindi-aware policy retrieval, and multipart audio/text interaction routes.
  * Built a responsive React/Vite/Tailwind chat experience with a browser audio recorder/player, sample questions, policy/claim cards, guided claim intake, and evidence uploads.
  * Expanded the database and application-flow documents to match the implementation and added local setup documentation.
* **Files Created/Modified:** `backend/`, `frontend/`, `README.md`, `brain/database_schema.md`, `brain/Agent_memory.md`.
* **Validation:** Python compilation, Vite production build, and backend route smoke tests pass, including policy/claim routes, document signature validation, upload/download, and missing-provider configuration handling.
* **Current Status:** MVP implementation complete. Provider endpoint URLs and credentials must be supplied in the environment to enable live AI voice interactions. No authentication is included; secure claim and policy data before handling real policyholder information.

### Prompt 3: Strict environment-based configuration
* **Actions Taken:**
  * Added a centralized immutable settings singleton, loaded from the backend `.env` file, and required project name, database URL, and upload directory values.
  * Routed the application, database, claim uploads, and all Gnani service clients through centralized settings; provider secrets/endpoints remain optional until live provider calls.
  * Added a local placeholder `.env`, committed template, and backend-specific `.gitignore` rule.
* **Files Created/Modified:** `backend/.env`, `backend/.env.example`, `backend/.gitignore`, `backend/app/config.py`, provider/API/database modules, `README.md`, `brain/Agent_memory.md`.
* **Validation:** Backend Python syntax compilation and TestClient startup passed using `backend/.env`; health, seeded policy, and missing Gnani configuration responses were verified.
* **Current Status:** Configuration refactor complete. Local Gnani keys and service endpoints are intentionally blank and must be set from the provider account before live voice calls.

### Prompt 4: Render/Neon seeding, policy endpoint, and CORS reliability
* **Actions Taken:**
  * Made demo seed records idempotent by natural keys, added a PostgreSQL advisory lock around seeding, and synchronized generated ID sequences to existing rows.
  * Adapted standard Neon PostgreSQL URLs to the psycopg 3 driver already listed in backend dependencies.
  * Exposed the policy list at both `/api/policies` and `/api/v1/policies`, and made results deterministic.
  * Normalized configured CORS origins and documented the required Render/Neon environment values; the frontend now surfaces policy-fetch errors instead of hiding their cause.
* **Validation:** TestClient preloaded a row with primary key `1`, ran seeding repeatedly, and verified no duplicate primary keys or duplicate demo records, existing and seeded policy results on both paths, plus Vercel CORS preflight. Backend syntax and frontend production build passed; standard/legacy PostgreSQL URL normalization was checked. Live Neon connectivity remains unverified from this workspace.
* **Current Status:** Deployment-hardening changes complete. Production Render/Neon environment values cannot be verified from this local workspace; set `DATABASE_URL` and `CORS_ORIGINS` in Render's environment.

### Prompt 5: Global API version prefix
* **Actions Taken:** Applied `/api/v1` once at the application router-inclusion layer and made policies, voice, and claims router paths relative to that shared prefix.
* **Files Modified:** `backend/app/main.py`, `backend/app/api/policies.py`, `backend/app/api/voice.py`, `backend/app/api/claims.py`, `brain/Agent_memory.md`.
* **Validation:** Confirmed the versioned policy, voice, and claims routes register once without duplicated `/api/v1` segments; backend compile and TestClient checks passed.

### Prompt 6: Vercel-to-Render API connectivity and CORS
* **Actions Taken:** Updated every frontend service request to build absolute `/api/v1` URLs from `VITE_API_BASE_URL`, with no localhost or relative URL fallback. Explicitly allowed the production Vercel origin in backend CORS and enabled OPTIONS preflight. Updated environment examples for the Render/Vercel deployment.
* **Files Modified:** `frontend/src/services/api.js`, `frontend/.env.example`, `backend/app/config.py`, `backend/app/main.py`, `backend/.env.example`, `brain/Agent_memory.md`.
* **Validation:** Frontend service-module search confirms no localhost or relative fetch URL; backend preflight and frontend production build passed.