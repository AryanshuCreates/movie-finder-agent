import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env (backend/.env)
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    # Fail fast with a very clear error instead of a cryptic GroqError
    raise RuntimeError(
        "GROQ_API_KEY is not set. "
        "Create backend/.env with GROQ_API_KEY=your_key and restart the server."
    )

client = Groq(api_key=api_key)

PROMPT_TEMPLATE = """
You are a movie understanding engine.
User query: "{query}"

Extract:
- Movie titles (if any)
- Genres
- Actors/Directors
- Keywords for TMDB search

Return as JSON:
{{
  "titles": [],
  "keywords": [],
  "actors": [],
  "directors": [],
  "genres": []
}}
"""

def analyze_query(query: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # or your chosen Groq model ID
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(query=query)}],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    # Very defensive: if LLM doesn't return clean JSON, fall back to simple keyword search
    try:
        parsed = eval(content)  # For a real project you'd use json.loads with a JSON-only prompt
        if not isinstance(parsed, dict):
            raise ValueError("Parsed content is not a dict")
        return {
            "titles": parsed.get("titles", []),
            "keywords": parsed.get("keywords", []),
            "actors": parsed.get("actors", []),
            "directors": parsed.get("directors", []),
            "genres": parsed.get("genres", []),
        }
    except Exception:
        # Safe fallback: just search TMDB using the raw query as keywords
        return {
            "titles": [],
            "keywords": [query],
            "actors": [],
            "directors": [],
            "genres": [],
        }
