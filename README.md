# GS420 AI
Open-source-first AI hub for Bengali + English chat, memory, vision, image, video, agents, tools and documents.

## Phase 11 — Document AI / RAG
Supports PDF, TXT/MD, CSV, DOCX and XLSX extraction, image upload for OCR workflows, persistent SQLite FTS5 lexical retrieval, document upload and search APIs. Semantic/vector retrieval can be added as an optional backend; this implementation does not claim semantic search from FTS5.

Run:
python -m uvicorn backend.main:app --reload

Full test command:
python scripts/test_all.py
