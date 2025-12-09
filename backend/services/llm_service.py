# backend/services/llm_service.py
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set. Add it to backend/.env")

client = Groq(api_key=api_key)

PROMPT_TEMPLATE = """
You are a focused movie-understanding engine. The user query may be:
- a movie title
- a plot description or partial scene
- a mood or tone (e.g. "something light and funny for date night")
- a genre combination or actor/director request
Treat the query as intent extraction only.

User query: "{query}"

Return a JSON object (ONLY JSON) with these keys:
{{
  "titles": [],       // explicit movie titles found (strings)
  "keywords": [],     // fallback search keywords / plot keywords
  "actors": [],       // actor names if mentioned
  "directors": [],    // director names if mentioned
  "genres": []        // genres if inferred
}}

Rules:
1) Always return valid JSON only (no extra text).
2) If no explicit title is present, put the core text as a single keyword entry.
3) Keep lists empty when nothing is found.
4) Keep responses short and deterministic.

Examples:
- "Mind-bending sci-fi movies like Inception" -> genres: ["Science Fiction"], keywords: ["mind-bending"], titles: ["Inception"]
- "A movie where a guy forgets his memory every day and falls in love" -> keywords: ["memory loss", "romance"], genres: []
"""

def analyze_query(query: str) -> dict:
    # Send prompt
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": PROMPT_TEMPLATE.format(query=query)}],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    # Try parse JSON safely
    try:
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("Parsed content is not an object")
        # Ensure keys exist
        return {
            "titles": parsed.get("titles", []),
            "keywords": parsed.get("keywords", []),
            "actors": parsed.get("actors", []),
            "directors": parsed.get("directors", []),
            "genres": parsed.get("genres", []),
        }
    except Exception:
        # Robust fallback: use raw query as a single keyword
        return {
            "titles": [],
            "keywords": [query],
            "actors": [],
            "directors": [],
            "genres": [],
        }
