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

    # Convert list → dict for fast lookup (SAFE VERSION)
    llm_map = {}

    for item in llm_results:
        try:
            idx = int(item.get("index"))  # 🔥 force int
            llm_map[idx] = item
        except:
            continue

    # -----------------------------
    # Step 4: Hybrid Scoring
    # -----------------------------
    final_results = []

    for i, candidate in enumerate(candidates):
        llm_data = llm_map.get(i + 1, {})
        
        # 🔍 DEBUG (add here)
        print("LLM MAP:", llm_map)
        print("INDEX LOOKUP:", i + 1)
        print("LLM DATA:", llm_data)

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

        # reasoning = llm_data.get("reasoning") or "Good skill match"
        if not llm_data.get("reasoning"):
            if llm_data.get("matched_skills"):
                reasoning = f"Matches skills: {', '.join(llm_data.get('matched_skills', []))}"
            else:
                reasoning = "Limited skill match for this role"
        else:
            reasoning = llm_data.get("reasoning")

        final_results.append({
            "name": candidate.get("name"),
            "title": candidate.get("title"),
            "final_score": round(final_score, 2),
            "vector_score": round(vector_score, 2),
            "llm_score": llm_score,
            "rule_score": r_score,
            "matched_skills": llm_data.get("matched_skills", []),
            "missing_skills": llm_data.get("missing_skills", []),
            "reasoning": reasoning   # ✅ use fixed value
        })

    # -----------------------------
    # Step 5: Sort Results
    # -----------------------------
    return sorted(final_results, key=lambda x: x["final_score"], reverse=True)