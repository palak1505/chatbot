from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

# retriever imports
from app.retriever.chunker import chunk_text
from app.retriever.store import add_chunks
from app.retriever.search import search_chunks

# LLM call (OpenRouter for now)
from app.llm.gemini_client import call_model

router = APIRouter()


# 📥 request schema
class ChatRequest(BaseModel):
    user_id: str
    message: str
    mode: str  # "guide" or "rag"


# 🟢 GUIDE MODE (mascot / onboarding)
def guide_response(message: str) -> str:
    prompt = f"""
You are a helpful product assistant.

Explain clearly and simply how the platform works.
Use step-by-step instructions if needed.

User question:
{message}
"""

    return f"[Guide Mode]\n{call_model(prompt)}"


# 🔵 RAG MODE (strict document-based)
def rag_response(message: str) -> str:
    results = search_chunks(message)

    if not results:
        return "[RAG Mode] I don't have enough information."

    # remove duplicates
    unique_results = list(dict.fromkeys(results))
    context = " ".join(unique_results)

    # 🔒 strict RAG prompt
    prompt = f"""
You are a helpful assistant.

Answer the question clearly and naturally using ONLY the provided context.

Do NOT say "based on context" or "according to context".
Just give the answer.

If the answer is not in the context, say:
"I don't have enough information."

Context:
{context}

Question:
{message}
"""

    answer = call_model(prompt)

    return f"[RAG Mode]\n{answer}"


# 💬 chat endpoint
@router.post("/chat")
def chat(req: ChatRequest):
    if req.mode == "guide":
        answer = guide_response(req.message)

    elif req.mode == "rag":
        answer = rag_response(req.message)

    else:
        answer = "Invalid mode"

    return {
        "user_id": req.user_id,
        "mode": req.mode,
        "response": answer
    }


# 📄 upload endpoint
@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")

    chunks = chunk_text(text)
    add_chunks(chunks)

    return {
        "message": "Document uploaded and processed",
        "chunks_added": len(chunks)
    }