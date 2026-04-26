from app.retriever.store import get_all_chunks


def search_chunks(query: str, top_k: int = 2):
    chunks = get_all_chunks()
    results = []

    for chunk in chunks:
        score = 0
        for word in query.lower().split():
            if word in chunk.lower():
                score += 1

        if score > 0:
            results.append((score, chunk))

    # sort by relevance
    results.sort(reverse=True, key=lambda x: x[0])

    return [chunk for _, chunk in results[:top_k]]