from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.retriever.store import get_all_chunks

MIN_SCORE = 0.1


def search_chunks(query: str, top_k: int = 3) -> list[str]:
    chunks = get_all_chunks()
    if not chunks:
        return []

    vectorizer = TfidfVectorizer()
    chunk_matrix = vectorizer.fit_transform(chunks)
    query_vector = vectorizer.transform([query])

    scores = cosine_similarity(query_vector, chunk_matrix)[0]

    scored = [
        (score, chunk)
        for score, chunk in zip(scores, chunks)
        if score >= MIN_SCORE
    ]
    scored.sort(reverse=True, key=lambda x: x[0])

    return [chunk for _, chunk in scored[:top_k]]
