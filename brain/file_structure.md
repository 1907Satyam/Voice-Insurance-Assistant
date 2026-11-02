voice-insurance-assistant/
│
├── brain/                             # Living Documentation & Agent Tracker
│   ├── PRD.md                         # Product Requirements Document
│   ├── TRD.md                         # Technical Requirements Document
│   ├── app_flow.md                    # End-to-End User Journeys & Sequence Flows
│   ├── database_schema.md             # SQL Tables, Entities & Relations
│   └── agent_memory.md                # Active Task Ledger (Requirements vs. Completed)
│
├── frontend/                          # React + Vite Frontend
│   ├── public/
│   │   └── favicon.ico
│   ├── src/
│   │   ├── assets/                    # Images, audio icons, logos
│   │   ├── components/
│   │   │   ├── VoiceRecorder.jsx      # Mic button, audio visualizer, waveform
│   │   │   ├── ChatBubble.jsx         # Voice transcript & response message display
│   │   │   ├── PolicyCard.jsx         # Summary cards for policy details
│   │   │   ├── ClaimStatusBadge.jsx   # Status tracker component
│   │   │   └── DocumentUploader.jsx   # Incident photo/document dropzone
│   │   ├── hooks/
│   │   │   ├── useAudioRecorder.js    # Web MediaRecorder API custom hook
│   │   │   └── useAudioPlayer.js      # Plays audio streams returned by Timbre TTS
│   │   ├── services/
│   │   │   └── api.js                 # Axios/Fetch API calls to FastAPI backend
│   │   ├── App.jsx                    # Main application layout
│   │   ├── index.css                  # Tailwind CSS styling
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── backend/                           # FastAPI Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI entrypoint, routes, CORS setup
│   │   ├── config.py                  # Environment variables & Gnani API keys
│   │   │
│   │   ├── api/                       # API Route Controllers
│   │   │   ├── __init__.py
│   │   │   ├── voice.py               # Audio upload, STT, and TTS endpoints
│   │   │   ├── policies.py            # Policy coverage & FAQ lookup endpoints
│   │   │   └── claims.py              # Claim registration & status endpoints
│   │   │
│   │   ├── services/                  # Gnani AI & Core Logic Services
│   │   │   ├── __init__.py
│   │   │   ├── prisma_stt.py          # Gnani Prisma API integration (Speech-to-Text)
│   │   │   ├── evon_llm.py            # Gnani Evon LLM integration (Intent & Reasoning)
│   │   │   ├── timbre_tts.py          # Gnani Timbre API integration (Text-to-Speech)
│   │   │   └── rag_engine.py          # Policy handbook retrieval / Vector Search
│   │   │
│   │   ├── db/                        # Database & Models
│   │   │   ├── __init__.py
│   │   │   ├── database.py            # SQLAlchemy engine setup
│   │   │   ├── models.py              # User, Policy, and Claim SQL schemas
│   │   │   └── seed_data.py           # Sample policy data (Hinglish/Hindi/English)
│   │   │
│   │   └── utils/                     # Utility functions
│   │       ├── audio.py               # Audio file format conversion (.webm -> .wav)
│   │       └── prompts.py             # Evon LLM system prompts (Hinglish context)
│   │
│   ├── uploads/                       # Temporary storage for incoming audio & photos
│   ├── data/                          # Policy PDFs / Vector Embeddings storage
│   ├── requirements.txt               # FastAPI, httpx, sqlalchemy, etc.
│   └── .env.example                   # Environment variable template
│
├── README.md                          # Project documentation & setup guide
└── .gitignore