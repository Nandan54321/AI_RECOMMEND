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
Job Requirement:
{query}

Candidates:
{text}

Return JSON list:
[
  {{
    "index": 1,
    "match_score": 0-100,
    "matched_skills": [],
    "missing_skills": [],
    "reasoning": ""
  }}
]
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

    res = requests.post(
        f"{url}/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )

    return res.json()["response"]

def analyze_batch(query, candidates):
    prompt = build_batch_prompt(query, candidates)

    try:
        output = call_local(prompt) if PROVIDER == "local" else call_openai(prompt)
        return json.loads(output)
    except:
        return []