from app.core.database import db

def vector_search_candidates(query_embedding):
    pipeline = [
        {
            "$vectorSearch": {
                "index": "resume_index",
                "path": "embedding",
                "queryVector": query_embedding,
                "numCandidates": 100,
                "limit": 5
            }
        },
        {
            "$project": {
                "_id": 0,
                "name": 1,
                "title": 1,
                "skills": 1,
                "resume_text": 1,
                "score": {"$meta": "vectorSearchScore"}
            }
        }
    ]
    return list(db.candidates.aggregate(pipeline))