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
You are an expert AI recruiter.

Job Requirement:
{query}

Candidates:
{text}

IMPORTANT:
- Return ONLY valid JSON
- No explanation text outside JSON
- No markdown
- Every candidate MUST have non-empty reasoning
- Reasoning must explain WHY the score is given

Format:
[
  {{
    "index": 1,
    "match_score": 75,
    "matched_skills": ["python"],
    "missing_skills": ["docker"],
    "reasoning": "Candidate has strong Python experience but lacks Docker which is required."
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
    