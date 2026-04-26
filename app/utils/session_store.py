# app/utils/session_store.py

USER_SESSIONS = {}


def get_user_session(user_id: str):
    if user_id not in USER_SESSIONS:
        USER_SESSIONS[user_id] = {
            "is_new_user": True,
            "mascot_enabled": True
        }
    return USER_SESSIONS[user_id]


def update_user_session(user_id: str, key: str, value):
    USER_SESSIONS[user_id][key] = value

def set_guide_step(user_id: str, step: int):
    USER_SESSIONS[user_id]["guide_step"] = step


def get_guide_step(user_id: str):
    return USER_SESSIONS[user_id].get("guide_step", 0)