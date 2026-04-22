import sys
import os

# -----------------------------
# Fix import path (important)
# -----------------------------
# Allows running script from project root:
# python scripts/seed.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import connect_to_mongo, close_mongo_connection
from app.db.seed import run_seed


# -----------------------------
# Main Script
# -----------------------------
def main():
    print("🚀 Manual DB Seeding Started...")

    try:
        # Step 1: Connect to DB
        connect_to_mongo()

        # Step 2: Run seed
        run_seed(n=120)  # you can change number here

        print("✅ Seeding completed successfully")

    except Exception as e:
        print(f"❌ Error during seeding: {e}")

    finally:
        # Step 3: Close connection
        close_mongo_connection()
        print("🔌 DB connection closed")


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()