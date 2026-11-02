# Product Requirements Document (PRD): Voice-First Vernacular Insurance Claim & Policy Assistant

## 1. Executive Summary & Problem Statement
Insurance penetration in Tier 2 and Tier 3 cities across India remains low due to significant friction points: dense English policy documentation, complex multi-page online forms, and cognitive overload when filing claims. Users naturally prefer speaking in conversational Hindi, Hinglish, or regional dialects. 

This project delivers a **full-stack voice-first vernacular insurance assistant** that eliminates language and literacy barriers, allowing users to check policy coverage, file claims through guided conversation, and check claim statuses entirely via natural voice interactions.

## 2. Target Audience & Personas
* **Semi-Urban / Rural Policyholder:** Comfortable speaking Hindi or Hinglish; struggles with reading fine-print policy terms or filling web forms on mobile devices.
* **First-Time Insurance Buyer:** Needs simplified, jargon-free explanations of what is covered (health, motor, term insurance).

## 3. Core Features & Scope
### F1: Voice Policy Navigator (RAG & FAQ)
* Users can ask questions about policy inclusions/exclusions verbally (e.g., *"Kya mera medical insurance ambulance ka kharcha cover karta hai?"*).
* System parses the query, queries policy documents, and responds instantly with voice and text.

### F2: Conversational Incident Reporting (Claim Intake)
* Replaces tedious multi-field claim forms with an interactive voice dialogue.
* Assistant guides the user step-by-step: Date/Time of incident, location, damage description, and photo/document upload.

### F3: Real-Time Claim Status Tracker
* Users can ask for status updates using their claim reference ID (e.g., *"Mere claim CLM-9842 ki kya sthiti hai?"*).

## 4. Success Metrics & Winning Differentiators
* **Zero Reading/Typing Load:** 100% voice-navigable interface.
* **Code-Mixed Hinglish Mastery:** High transcription accuracy on noisy audio inputs using Gnani Prisma STT.
* **Human-like Empathetic Response:** Natural tone synthesis via Gnani Timbre TTS.