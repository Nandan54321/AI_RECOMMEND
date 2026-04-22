from faker import Faker
import random

from app.core.database import get_collection
from app.services.embeddings import get_embeddings


fake = Faker()

# -----------------------------
# Sample Skills Pool
# -----------------------------
SKILLS_POOL = [
    "Python", "Java", "C++", "Machine Learning", "Deep Learning",
    "NLP", "Computer Vision", "TensorFlow", "PyTorch",
    "FastAPI", "Django", "Flask", "MongoDB", "SQL",
    "AWS", "Docker", "Kubernetes", "Git", "Linux",
    "Data Analysis", "Pandas", "NumPy", "Scikit-learn",
    "React", "Node.js", "REST APIs"
]


# -----------------------------
# Generate Single Candidate
# -----------------------------
def generate_candidate():
    name = fake.name()
    title = random.choice([
        "Software Engineer",
        "ML Engineer",
        "Data Scientist",
        "Backend Developer",
        "AI Engineer"
    ])

    skills = random.sample(SKILLS_POOL, k=random.randint(5, 10))

    experience = random.randint(1, 10)

    resume_text = f"""
    {name} is a {title} with {experience} years of experience.
    Skilled in {', '.join(skills)}.
    Worked on real-world applications and scalable systems.
    """

    return {
        "name": name,
        "title": title,
        "skills": skills,
        "resume_text": resume_text.strip()
    }


# -----------------------------
# Seed Database
# -----------------------------
def run_seed(n: int = 120):
    candidates_col = get_collection("candidates")

    # -----------------------------
    # Prevent duplicate seeding
    # -----------------------------
    existing_count = candidates_col.count_documents({})

    if existing_count >= n:
        print(f"⚡ Already seeded with {existing_count} candidates")
        return

    print(f"🌱 Seeding {n} candidates...")

    # -----------------------------
    # Generate candidates
    # -----------------------------
    candidates = [generate_candidate() for _ in range(n)]

    # -----------------------------
    # Generate embeddings (batch)
    # -----------------------------
    texts = [c["resume_text"] for c in candidates]
    embeddings = get_embeddings(texts)

    for i, c in enumerate(candidates):
        c["embedding"] = embeddings[i]

    # -----------------------------
    # Insert into DB
    # -----------------------------
    candidates_col.insert_many(candidates)

    print(f"✅ Inserted {len(candidates)} candidates into database")