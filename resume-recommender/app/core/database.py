from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.core.config import settings


# -----------------------------
# MongoDB Client (Singleton)
# -----------------------------
class MongoDB:
    client: MongoClient = None
    db = None


mongodb = MongoDB()


# -----------------------------
# Connect to MongoDB
# -----------------------------
def connect_to_mongo():
    if mongodb.client is None:
        try:
            mongodb.client = MongoClient(
                settings.MONGO_URI,
                maxPoolSize=50,          # connection pool size
                minPoolSize=5,
                serverSelectionTimeoutMS=5000
            )

            # Verify connection
            mongodb.client.admin.command("ping")

            mongodb.db = mongodb.client[settings.DB_NAME]

            print("✅ Connected to MongoDB")

        except ConnectionFailure as e:
            raise RuntimeError(f"❌ MongoDB connection failed: {e}")


# -----------------------------
# Close MongoDB Connection
# -----------------------------
def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()
        print("🔌 MongoDB connection closed")


# -----------------------------
# Get DB Instance
# -----------------------------
def get_db():
    if mongodb.db is None:
        connect_to_mongo()
    return mongodb.db


# -----------------------------
# Helper: Get Collection
# -----------------------------
def get_collection(name: str):
    return get_db()[name]