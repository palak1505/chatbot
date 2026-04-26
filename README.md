# 🤖 AI Mascot Assistant Backend

A modular AI backend built with FastAPI that combines:

* 🟢 Guide Mode (product assistant / onboarding)
* 🔵 RAG Mode (document-based Q&A)

---

## 🚀 Features

* FastAPI backend
* Document upload & processing
* Chunking + retrieval system
* RAG (Retrieval-Augmented Generation)
* LLM integration (via OpenRouter, replaceable)
* Guide mode for user onboarding
* Clean modular architecture

---

## 🧠 How It Works

### Guide Mode

* Explains how the platform works
* Uses LLM directly
* No document restriction

### RAG Mode

* Retrieves relevant document chunks
* Sends context to LLM
* Strictly answers from documents
* Prevents hallucination

---

## 🔁 Flow

```
User → API → Mode Selection
     → Guide → LLM → Answer
     → RAG → Retrieve → LLM → Answer
```

---

## 📁 Project Structure

```
app/
├── api/            # FastAPI routes
├── agent/          # core logic (future expansion)
├── retriever/      # chunking, storage, search
├── llm/            # model integration
```

---

## ⚙️ Setup

### 1. Install dependencies

```
pip install fastapi uvicorn python-multipart requests python-dotenv
```

### 2. Add environment variables

Create `.env`:

```
OPENROUTER_API_KEY=your_api_key
```

---

### 3. Run server

```
uvicorn main_api:app --reload
```

---

### 4. Test API

Open:

```
http://127.0.0.1:8000/docs
```

---

## 📄 Endpoints

### POST `/upload`

Upload a `.txt` file → chunked and stored

### POST `/chat`

```json
{
  "user_id": "1",
  "message": "your question",
  "mode": "guide" // or "rag"
}
```

---

## 🧭 Roadmap

* [ ] Session-based mascot behavior
* [ ] Improved retrieval accuracy
* [ ] Vector database (Supabase pgvector)
* [ ] Persistent storage
* [ ] Frontend integration
* [ ] Multi-project support

---

## 🧩 Design Philosophy

* Modular LLM layer (swap providers easily)
* Clear separation of Guide vs RAG
* Backend-first development
* Incremental complexity

---

## ⚠️ Notes

* `.env` is ignored (API keys are safe)
* Current retrieval is keyword-based (no embeddings yet)
* Designed for scalability

---

## 🎯 Goal

Build a reusable AI assistant that acts as a “mascot” for any platform, helping users both:

* learn the system (Guide Mode)
* query knowledge (RAG Mode)
