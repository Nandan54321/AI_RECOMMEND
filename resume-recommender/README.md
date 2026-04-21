# AI Resume Recommender 🚀

## Features
- Vector Search (MongoDB)
- Hybrid Ranking (Vector + LLM + Rules)
- Batch LLM (cost optimized)
- OpenAI + Local LLM support
- Recruiter Dashboard (Streamlit)

## Setup

```bash
git clone <repo>
cd resume-recommender
pip install -r requirements.txt

## Project Structure
resume-recommender/
├── app/
│   ├── main.py
│
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   └── search.py
│   │       └── router.py
│
│   ├── services/
│   │   ├── embeddings.py
│   │   ├── search_service.py
│   │   ├── llm_service.py
│   │   └── scorer.py
│
│   ├── repositories/
│   │   └── candidate_repo.py
│
│   ├── db/
│   │   └── seed.py
│
│   └── models/
│       └── candidate.py
│
├── dashboard/
│   └── app.py
│
├── scripts/
│   └── seed.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md