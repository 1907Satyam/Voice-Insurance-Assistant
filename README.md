# Aawaaz — Voice-First Insurance Assistant

A mobile-first Hindi/Hinglish insurance assistant with a FastAPI backend and a
React/Vite frontend. It provides sample policy data, claim status lookup and
creation, and configurable integrations for Gnani Prisma STT, Evon LLM, and
Timbre TTS.

## Requirements

- Python 3.10+
- Node.js 18+
- Gnani API access and the provider endpoint URLs for live voice conversations

## Run the backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Fill GNANI_API_KEY_ID and the three provider URLs in .env
uvicorn app.main:app --reload
```

The API listens on `http://localhost:8000`; OpenAPI docs are at `/docs`.
Database tables and demo data are initialized on startup. By default SQLite
stores its file at `backend/data/insurance_assistant.db`.

## Run the frontend

```powershell
cd frontend
npm install
Copy-Item .env.example .env
npm run dev
```

Set `VITE_API_BASE_URL` when the backend is hosted somewhere other than
`http://localhost:8000`. Browser microphone access requires localhost or HTTPS.

## API routes

- `POST /api/v1/voice/interact` — audio multipart field `audio`, optional `language`
- `POST /api/v1/voice/interact/text` — text-only interaction for sample prompts
- `GET /api/v1/policies` — sample policies
- `POST /api/v1/claims` — create a claim record
- `GET /api/v1/claims/{reference_id}` — claim status
- `POST /api/v1/claims/{reference_id}/documents` — attach PDF/JPEG/PNG/WebP documents
- `GET /api/v1/claims/{reference_id}/documents/{document_id}` — download an attachment
- `GET /health` — health check

## Provider configuration

Copy `backend/.env.example` to `backend/.env` and set `GNANI_API_KEY_ID`,
`PRISMA_STT_URL`, `EVON_LLM_URL`, and `TIMBRE_TTS_URL` to the exact endpoints
supplied for your Gnani account. `PROJECT_NAME`, `DATABASE_URL`, and `UPLOAD_DIR`
are required configuration values. The application does not guess provider hosts. Requests use the
`X-API-Key-ID` header; Evon is expected to accept an OpenAI-compatible chat
completion request and return JSON content with `intent` and `response`.

## Render and Vercel deployment

Configure these values in Render's backend environment (the ignored local
`backend/.env` file is not deployed):

- `PROJECT_NAME=Voice Insurance Assistant`
- `DATABASE_URL` — Neon PostgreSQL URL. Standard `postgresql://` and legacy
  `postgres://` URLs are adapted to the installed psycopg 3 driver.
- `UPLOAD_DIR` — for example `/opt/render/project/src/backend/uploads`. Use a
  persistent disk or external object storage if uploaded documents must survive
  Render instance replacement.
- `CORS_ORIGINS=https://voice-insurance-assistant.vercel.app` (add any other
  trusted frontend origins as comma-separated values).
- The Gnani provider key ID and URLs for live voice interactions.

The policy list is available at both `/api/policies` and
`/api/v1/policies`. Startup seeding checks natural keys before adding demo rows
and synchronizes PostgreSQL generated-ID sequences to existing table values.
The seed operation uses a PostgreSQL advisory lock so concurrent Render
instances do not insert the same demo records at once.

## Production checklist

This repository is a runnable MVP, not a deployment-ready insurance system.
Before real customer use, add authentication and authorization, encrypted
storage and retention controls, persistent claim-document handling, provider
timeouts/retries and operational monitoring, migrations, secrets management,
and legal/compliance review. Seed records and policy clauses are illustrative,
not insurance advice or actual coverage commitments.
