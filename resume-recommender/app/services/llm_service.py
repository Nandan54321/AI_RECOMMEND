import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "openai")

def build_batch_prompt(query, candidates):
    text = "\n".join([
        f"{i+1}. {c['resume_text']}"
        for i, c in enumerate(candidates)
    ])

    return f"""
You are a senior technical recruiter and hiring expert.

Your task is to evaluate how well each candidate matches the job requirement.

JOB REQUIREMENT:
{query}

CANDIDATES:
{text}


### SCORING RULES (STRICT):
Evaluate each candidate using the following weighted criteria:

1. Skills Match (40%)
   - Compare required vs candidate skills
   - Exact and related skills both count
   - Infer skills from projects and experience even if not explicitly listed

2. Experience Relevance (25%)
   - Relevant domain/project experience
   - Real-world usage of required skills

3. Tools & Technologies (15%)
   - Frameworks, libraries, platforms

4. Education / Certifications (10%)
   - Relevant degrees or certifications

5. Overall Fit & Context (10%)
   - Role alignment, clarity, and depth

### SCORING INSTRUCTIONS:
- Score MUST be between 0 and 100
- Be consistent across candidates
- High score (80+) ONLY if strong match across most categories
- Low score (<50) if major requirements are missing
- Ensure score distribution is meaningful (avoid giving all candidates similar scores)

### OUTPUT FORMAT (STRICT JSON ONLY):
Return ONLY a JSON array. No extra text.

[
  {{
    "index": 1,
    "match_score": 78,
    "matched_skills": ["python", "fastapi"],
    "missing_skills": ["docker", "kubernetes"],
    "reasoning": "Candidate has strong backend experience using Python and FastAPI with relevant projects. However, lacks containerization tools like Docker and Kubernetes, which reduces overall match."
  }}
]

### IMPORTANT RULES:
- DO NOT return markdown
- DO NOT add explanations outside JSON
- Reasoning MUST be specific and non-empty
- Mention BOTH strengths and gaps in reasoning
- Keep reasoning concise (2–4 sentences)
- Do NOT assume skills that are not supported by the resume
- Follow ALL rules strictly. If output is not valid JSON or violates any rule, it will be rejected.
"""

def call_openai(prompt):
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return res.choices[0].message.content

def call_local(prompt):
    url = os.getenv("OLLAMA_URL")
    model = os.getenv("OLLAMA_MODEL")

    try:
        res = requests.post(
            f"{url}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=30
        )
        return res.json().get("response", "")
    except Exception as e:
        print("LLM ERROR:", e)
        return ""

import re

def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        # extract JSON array using regex
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return []
        return []

def analyze_batch(query, candidates):
    prompt = build_batch_prompt(query, candidates)

    try:
        output = call_local(prompt) if PROVIDER == "local" else call_openai(prompt)
        print("LLM RAW OUTPUT:\n", output)
        return safe_json_parse(output)

    except:
        return []
    