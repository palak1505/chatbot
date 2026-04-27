import io
from fastapi import APIRouter, UploadFile, File, HTTPException
import docx
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

STEP_CONTENT = {
    1: "Step 1: Type any question in the chat box below and hit Send. I'll do my best to help!",
    2: "Step 2: Use the Upload section at the bottom to add a document (.txt or .docx). I'll read it and answer questions based on it.",
    3: "Step 3: Once your document is uploaded, just ask me anything about it — I'll find the answer for you.",
}

INTENT_KEYWORDS = {
    "dashboard": ["chat", "question", "ask", "type", "message", "start", "begin", "send"],
    "reports":   ["upload", "document", "file", "add", "attach", "docx", "txt", "import"],
    "upload":    ["answer", "find", "search", "query", "about", "tell me", "what is"],
    "skip":      ["skip", "next", "continue", "already", "got it", "ok", "okay", "yes", "know", "move on"],
    "help":      ["help", "confused", "lost", "repeat", "again", "explain", "don't understand"],
}

TOPIC_TO_STEP = {"dashboard": 1, "reports": 2, "upload": 3}


def detect_intent(message: str) -> str:
    msg = message.lower()
    scores = {
        intent: sum(1 for kw in keywords if kw in msg)
        for intent, keywords in INTENT_KEYWORDS.items()
    }
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "unknown"


# 📥 request schema
class ChatRequest(BaseModel):
    user_id: str
    message: str
    mode: str | None = None  # "guide" or "rag" — overrides auto-detection


# 🟢 GUIDE MODE (intent-aware onboarding)
def guide_response(user_id: str, message: str) -> str:
    step = get_guide_step(user_id)

    if step == 0:
        set_guide_step(user_id, 1)
        return f"[Guide Mode]\nWelcome! I'll walk you through the platform.\n\n{STEP_CONTENT[1]}"

    if step > 3:
        return "[Guide Mode]\nYou're all set! You can ask me specific questions anytime."

    intent = detect_intent(message)

    # User asks about a specific topic — jump forward to it
    if intent in TOPIC_TO_STEP:
        target = TOPIC_TO_STEP[intent]
        if target >= step:
            set_guide_step(user_id, target + 1)
            prefix = "Great question! Let me jump to that.\n\n" if target != step else ""
            return f"[Guide Mode]\n{prefix}{STEP_CONTENT[target]}"

    # User wants to skip / move on
    if intent == "skip":
        next_step = step + 1
        if next_step > 3:
            set_guide_step(user_id, 4)
            return "[Guide Mode]\nYou're all set! You can ask me specific questions anytime."
        set_guide_step(user_id, next_step)
        return f"[Guide Mode]\n{STEP_CONTENT[next_step]}"

    # User is confused — re-explain current step without advancing
    if intent == "help":
        return f"[Guide Mode]\nNo problem, here's what to do:\n\n{STEP_CONTENT[step]}"

    # Default — advance to next step
    next_step = step + 1
    set_guide_step(user_id, next_step)
    if next_step > 3:
        return "[Guide Mode]\nYou're all set! You can ask me specific questions anytime."
    return f"[Guide Mode]\n{STEP_CONTENT[next_step]}"


# 🔵 RAG MODE (strict)
def rag_response(message: str) -> str:
    results = search_chunks(message)

    if not results:
        return "[RAG Mode] I don't have enough information."

    context = "\n\n".join(results)

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

    # 🧠 decide mode
    if req.mode in ("guide", "rag"):
        mode = req.mode
        if mode == "guide" and get_guide_step(req.user_id) > 3:
            set_guide_step(req.user_id, 0)
    elif session["is_new_user"] and session["mascot_enabled"]:
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
    filename = file.filename.lower()

    if filename.endswith(".docx"):
        doc = docx.Document(io.BytesIO(content))
        text = "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    elif filename.endswith(".txt"):
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin-1")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload a .txt or .docx file.")

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