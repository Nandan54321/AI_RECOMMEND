# from fastapi import FastAPI
# from contextlib import asynccontextmanager

# from app.api.v1.router import api_router
# from app.db.seed import run_seed


# # -----------------------------
# # Lifespan (Startup / Shutdown)
# # -----------------------------
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     print("🚀 Starting AI Resume Recommender...")

#     # Safe seeding (won't duplicate if already seeded)
#     try:
#         run_seed()
#         print("🌱 Database ready")
#     except Exception as e:
#         print(f"⚠️ Seeding skipped or failed: {e}")

#     yield

#     print("🛑 Shutting down application...")


# # -----------------------------
# # FastAPI App
# # -----------------------------
# app = FastAPI(
#     title="AI Resume Recommender",
#     description="Hybrid AI system (Vector Search + LLM + Rules)",
#     version="1.0.0",
#     lifespan=lifespan
# )


# # -----------------------------
# # Routers
# # -----------------------------
# app.include_router(api_router, prefix="/api/v1")


# # -----------------------------
# # Health Check
# # -----------------------------
# @app.get("/")
# def root():
#     return {
#         "message": "AI Resume Recommender is running 🚀",
#         "docs": "/docs"
#     }


# @app.get("/health")
# def health_check():
#     return {"status": "ok"}

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.v1.router import api_router
from app.db.seed import run_seed
from app.core.database import connect_to_mongo, close_mongo_connection


# -----------------------------
# Lifespan (Startup / Shutdown)
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting AI Resume Recommender...")

    # ✅ Step 1: Connect to MongoDB FIRST
    try:
        connect_to_mongo()
    except Exception as e:
        print(f"❌ DB connection failed: {e}")
        raise e

    # ✅ Step 2: Seed DB AFTER connection
    try:
        run_seed()
        print("🌱 Database ready")
    except Exception as e:
        print(f"⚠️ Seeding skipped or failed: {e}")

    yield

    # ✅ Step 3: Close DB on shutdown
    close_mongo_connection()
    print("🛑 Shutting down application...")


# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(
    title="AI Resume Recommender",
    description="Hybrid AI system (Vector Search + LLM + Rules)",
    version="1.0.0",
    lifespan=lifespan
)


# -----------------------------
# Routers
# -----------------------------
app.include_router(api_router, prefix="/api/v1")


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "AI Resume Recommender is running 🚀",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}