# from app.services.embeddings import get_embedding
# from app.repositories.candidate_repo import vector_search_candidates
# from app.services.llm_service import analyze_batch
# from app.services.scorer import rule_score

# def search_candidates(query: str):

#     query_embedding = get_embedding(query)
    
#     if not query_embedding:
#         raise ValueError("Query cannot be empty")
    
#     candidates = vector_search_candidates(query_embedding)

#     llm_results = analyze_batch(query, candidates)

#     final = []

#     for i, c in enumerate(candidates):
#         llm = next((x for x in llm_results if x["index"] == i+1), {})

#         r_score = rule_score(query, c["skills"])

#         final_score = (
#             0.5 * c["score"] * 100 +
#             0.4 * llm.get("match_score", 0) +
#             0.1 * r_score
#         )

#         final.append({
#             "name": c["name"],
#             "title": c["title"],
#             "final_score": round(final_score, 2),
#             **llm
#         })

#     return sorted(final, key=lambda x: x["final_score"], reverse=True)

from app.services.embeddings import get_embedding
from app.repositories.candidate_repo import vector_search_candidates
from app.services.llm_service import analyze_batch
from app.services.scorer import rule_score


def search_candidates(query: str):
    """
    Main search pipeline:
    1. Convert query → embedding
    2. Retrieve candidates via vector search
    3. Run batch LLM scoring
    4. Apply rule-based scoring
    5. Compute hybrid final score
    """

    # -----------------------------
    # Step 1: Generate embedding
    # -----------------------------
    query = query.strip()

    if not query:
        raise ValueError("Query cannot be empty")

    query_embedding = get_embedding(query)

    if not query_embedding:
        raise ValueError("Failed to generate embedding")

    # -----------------------------
    # Step 2: Vector Search
    # -----------------------------
    candidates = vector_search_candidates(query_embedding)

    if not candidates:
        return []

    # -----------------------------
    # Step 3: LLM Batch Scoring
    # -----------------------------
    llm_results = analyze_batch(query, candidates)

    # Convert list → dict for fast lookup
    llm_map = {
        item.get("index"): item
        for item in llm_results
        if isinstance(item, dict) and "index" in item
    }

    # -----------------------------
    # Step 4: Hybrid Scoring
    # -----------------------------
    final_results = []

    for i, candidate in enumerate(candidates):
        llm_data = llm_map.get(i + 1, {})

        # Rule-based score
        r_score = rule_score(query, candidate.get("skills", []))

        # LLM score (safe fallback)
        llm_score = llm_data.get("match_score", 0)

        # Vector score (0–1 → 0–100)
        vector_score = candidate.get("score", 0) * 100

        # Hybrid scoring formula
        final_score = (
            0.5 * vector_score +
            0.4 * llm_score +
            0.1 * r_score
        )

        final_results.append({
            "name": candidate.get("name"),
            "title": candidate.get("title"),
            "final_score": round(final_score, 2),
            "vector_score": round(vector_score, 2),
            "llm_score": llm_score,
            "rule_score": r_score,
            "matched_skills": llm_data.get("matched_skills", []),
            "missing_skills": llm_data.get("missing_skills", []),
            "reasoning": llm_data.get("reasoning", "No reasoning available")
        })

    # -----------------------------
    # Step 5: Sort Results
    # -----------------------------
    return sorted(final_results, key=lambda x: x["final_score"], reverse=True)