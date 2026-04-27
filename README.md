# AI Mascot Assistant

An AI-powered assistant that combines guided onboarding (Mascot) and document-based Q&A (RAG) into a single modular backend.

---

## Features

**Guide Mode (Mascot)**
- Automatically triggered for new users
- Intent-aware onboarding — detects what the user is asking about and jumps to the relevant step
- Supports skip, help, and topic-jump intents via keyword detection
- Can be manually toggled from the UI (Auto / Guide / RAG)
- Step progress persisted in Supabase

**RAG Mode**
- Upload `.txt` or `.docx` documents
- TF-IDF retrieval with cosine similarity scoring
- Score threshold filters out irrelevant chunks before sending to LLM
- Strict anti-hallucination prompt — answers only from uploaded context

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI |
| LLM | OpenRouter (meta-llama/llama-3-8b-instruct) |
| Retrieval | TF-IDF + cosine similarity (scikit-learn) |
| Sessions | Supabase (Postgres) |
| Frontend | HTML + CSS + JS (Live Server) |

---

## Project Structure

```
app/
├── api/
│   └── routes.py        # /chat, /upload, /mascot/toggle endpoints
├── retriever/
│   ├── chunker.py        # word-based text splitting
│   ├── store.py          # in-memory document store
│   └── search.py         # TF-IDF retrieval with score threshold
├── llm/
│   └── gemini_client.py  # OpenRouter API wrapper
└── utils/
    └── session_store.py  # Supabase-backed session management

config/
└── settings.py           # env var loading

index.html                # chat UI
main_api.py               # FastAPI entry point
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env`

```
OPENROUTER_API_KEY=your_openrouter_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
```

### 3. Create Supabase table

Run in Supabase SQL Editor:

```sql
create table user_sessions (
    user_id text primary key,
    is_new_user boolean default true,
    mascot_enabled boolean default true,
    guide_step integer default 0,
    updated_at timestamp default now()
);

alter table user_sessions disable row level security;
```

### 4. Run the server

```bash
uvicorn main_api:app --reload
```

### 5. Open the UI

Open `index.html` via VS Code Live Server.

---

## API Endpoints

### `POST /chat`

```json
{
  "user_id": "user_1",
  "message": "how do I upload a file?",
  "mode": null
}
```

`mode` is optional — pass `"guide"` or `"rag"` to override auto-detection, or omit for automatic.

### `POST /upload`

Upload a `.txt` or `.docx` file. Returns chunk count.

### `POST /mascot/toggle`

```
?user_id=user_1&enable=true
```

---

## Flow

```
User → UI → POST /chat
         → Auto mode: new user → Guide Mode
                      returning user → RAG Mode
         → Manual mode: forced Guide or RAG

Guide Mode → intent detection → step response
RAG Mode   → TF-IDF search → top-K chunks → LLM → answer
```

---

## Roadmap

- [x] TF-IDF retrieval with score threshold
- [x] Intent-aware mascot (skip, help, topic jump)
- [x] Supabase session persistence
- [x] .docx upload support
- [x] Mode toggle in UI (Auto / Guide / RAG)
- [ ] Semantic search with embeddings
- [ ] Multi-project / knowledge base support
- [ ] React frontend
- [ ] User authentication
