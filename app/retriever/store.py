# simple in-memory store (later → DB / Supabase)

DOCUMENT_STORE = []


def add_chunks(chunks):
    for chunk in chunks:
        DOCUMENT_STORE.append(chunk)


def get_all_chunks():
    return DOCUMENT_STORE