# 🤖 AI Mascot Assistant

An AI-powered assistant that combines:

* 🟢 Guided onboarding (Mascot Mode)
* 🔵 Document-based Q&A (RAG Mode)

---

## 🚀 Features

* FastAPI backend
* Basic UI (HTML + Live Server)
* Document upload + processing
* Chunking + retrieval system
* RAG (Retrieval-Augmented Generation)
* LLM integration (OpenRouter, replaceable)
* Session-based mascot behavior

---

## 🧠 How It Works

### 🟢 Guide Mode (Mascot)

* Automatically triggered for new users
* Walks users through the platform step-by-step
* Provides onboarding assistance
* Intent-aware (basic keyword detection)

---

### 🔵 RAG Mode

* Retrieves relevant document chunks
* Sends context to LLM
* Generates answers strictly from documents
* Prevents hallucination

---

## 🔁 Flow

```id="flow1"
User → UI → API → Session Check
     → Guide Mode → LLM → Answer
     → RAG Mode → Retrieve → LLM → Answer
```

---

## 📁 Project Structure

```id="flow2"
app/
├── api/            # FastAPI routes
├── retriever/      # chunking, storage, search
├── llm/            # LLM integration
├── utils/          # session handling

index.html          # basic UI
main_api.py         # FastAPI entry
```

---

## ⚙️ Setup

### 1. Install dependencies

```id="cmd1"
pip install fastapi uvicorn python-multipart requests python-dotenv
```

---

### 2. Add environment variables

Create `.env`:

```id="cmd2"
OPENROUTER_API_KEY=your_api_key
```

---

### 3. Run backend

```id="cmd3"
uvicorn main_api:app --reload
```

---

### 4. Run UI

Use VS Code **Live Server** on:

```id="cmd4"
index.html
```

---

## 📄 API Endpoints

### POST `/upload`

Upload `.txt` file → chunked and stored

### POST `/chat`

```json id="cmd5"
{
  "user_id": "1",
  "message": "your question"
}
```

---

## 🧭 Roadmap

* [ ] Improve mascot intelligence
* [ ] Improve retrieval accuracy
* [ ] Add embeddings (semantic search)
* [ ] Persist sessions (Supabase)
* [ ] Improve UI (React)
* [ ] Multi-project support

---

## 🧩 Design Philosophy

* Backend-driven logic
* Modular LLM layer
* Clear separation of Guide vs RAG
* Incremental complexity
* Avoid overengineering early

---

## ⚠️ Notes

* Sessions are in-memory (reset on restart)
* Retrieval is keyword-based
* UI is for testing purposes

---

## 🎯 Goal

Build a reusable AI assistant that can act as a **“mascot” for any platform**, helping users:

* understand the system (Guide Mode)
* query knowledge (RAG Mode)
