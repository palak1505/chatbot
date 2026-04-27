from datetime import datetime, timezone
from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_KEY

_client = create_client(SUPABASE_URL, SUPABASE_KEY)
_table = "user_sessions"


def _fetch(user_id: str) -> dict | None:
    result = _client.table(_table).select("*").eq("user_id", user_id).execute()
    return result.data[0] if result.data else None


def get_user_session(user_id: str) -> dict:
    row = _fetch(user_id)
    if not row:
        _client.table(_table).insert({"user_id": user_id}).execute()
        return {"is_new_user": True, "mascot_enabled": True, "guide_step": 0}
    return row


def update_user_session(user_id: str, key: str, value) -> None:
    _client.table(_table).update({key: value, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("user_id", user_id).execute()


def get_guide_step(user_id: str) -> int:
    row = _fetch(user_id)
    return row["guide_step"] if row else 0


def set_guide_step(user_id: str, step: int) -> None:
    _client.table(_table).update({"guide_step": step, "updated_at": datetime.now(timezone.utc).isoformat()}).eq("user_id", user_id).execute()
