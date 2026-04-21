from app.services.embeddings import get_embedding
from app.repositories.candidate_repo import vector_search_candidates
from app.services.llm_service import analyze_batch
from app.services.scorer import rule_score

def search_candidates(query: str):
    query_embedding = get_embedding(query)
    candidates = vector_search_candidates(query_embedding)

    llm_results = analyze_batch(query, candidates)

    final = []

    for i, c in enumerate(candidates):
        llm = next((x for x in llm_results if x["index"] == i+1), {})

        r_score = rule_score(query, c["skills"])

        final_score = (
            0.5 * c["score"] * 100 +
            0.4 * llm.get("match_score", 0) +
            0.1 * r_score
        )

        final.append({
            "name": c["name"],
            "title": c["title"],
            "final_score": round(final_score, 2),
            **llm
        })

    return sorted(final, key=lambda x: x["final_score"], reverse=True)