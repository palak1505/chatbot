from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

# retriever
from app.retriever.chunker import chunk_text
from app.retriever.store import add_chunks
from app.retriever.search import search_chunks

# LLM
from app.llm.gemini_client import call_model

# session
from app.utils.session_store import (
    get_user_session,
    update_user_session,
    get_guide_step,
    set_guide_step
)

router = APIRouter()


# 📥 request schema
class ChatRequest(BaseModel):
    user_id: str
    message: str


# 🟢 GUIDE MODE (structured onboarding)
def guide_response(user_id: str, message: str) -> str:
    step = get_guide_step(user_id)

    if step == 0:
        set_guide_step(user_id, 1)
        return "[Guide Mode]\nWelcome! Let me walk you through the platform.\n\nStep 1: Go to the dashboard to see an overview."

    elif step == 1:
        set_guide_step(user_id, 2)
        return "[Guide Mode]\nStep 2: Navigate to the Reports section to view all documents."

    elif step == 2:
        set_guide_step(user_id, 3)
        return "[Guide Mode]\nStep 3: Use the upload button on the top right to add new documents."

    elif step == 3:
        return "[Guide Mode]\nYou're all set! You can now explore or ask specific questions anytime."

    # fallback (user asks something specific)
    prompt = f"""
You are a helpful product assistant.

Explain clearly and simply how the platform works.

User question:
{message}
"""
    return f"[Guide Mode]\n{call_model(prompt)}"


# 🔵 RAG MODE (strict)
def rag_response(message: str) -> str:
    results = search_chunks(message)

    if not results:
        return "[RAG Mode] I don't have enough information."

    # remove duplicates
    unique_results = list(dict.fromkeys(results))
    context = " ".join(unique_results)

    prompt = f"""
You are a helpful assistant.

Answer clearly and naturally using ONLY the provided context.
Do NOT say "based on context".

If the answer is not in the context, say:
"I don't have enough information."

Context:
{context}

Question:
{message}
"""

    answer = call_model(prompt)

    return f"[RAG Mode]\n{answer}"


# 💬 chat endpoint (AUTO MODE)
@router.post("/chat")
def chat(req: ChatRequest):
    session = get_user_session(req.user_id)

    # 🧠 decide mode automatically
    if session["is_new_user"] and session["mascot_enabled"]:
        mode = "guide"
        update_user_session(req.user_id, "is_new_user", False)
    else:
        mode = "rag"

    # 🔁 route
    if mode == "guide":
        answer = guide_response(req.user_id, req.message)
    else:
        answer = rag_response(req.message)

    return {
        "user_id": req.user_id,
        "mode_used": mode,
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


# 🔁 mascot toggle endpoint
@router.post("/mascot/toggle")
def toggle_mascot(user_id: str, enable: bool):
    update_user_session(user_id, "mascot_enabled", enable)

    return {
        "message": f"Mascot {'enabled' if enable else 'disabled'}"
    }