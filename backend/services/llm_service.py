import os
import json
import logging
from string import Template
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set. Add it to backend/.env")

client = Groq(api_key=api_key)

PROMPT_TEMPLATE = Template(r"""
You are a focused movie-understanding engine. The user query may be:
- a movie title
- a plot description or partial scene
- a mood or tone (e.g. "something light and funny for date night")
- a genre combination or actor/director request

Your job is to extract intent **and** — when the user does NOT supply a clear movie title —
provide a single recommended movie title that best matches the query (a well-known example
or the best fitting movie). This helps map vague descriptions to an actual movie to search.

User query: "$query"

Return a JSON object (ONLY JSON) with these keys:
{
  "titles": [],       // If query contains explicit title(s) list them. 
                      // If no explicit title present, include one recommended movie title (single string).
  "keywords": [],     // fallback search keywords / plot keywords
  "actors": [],       // actor names if mentioned
  "directors": [],    // director names if mentioned
  "genres": []        // genres if inferred
}

Rules:
1) Always return valid JSON only (no extra text).
2) If you add a recommended title when none was provided, prefer a well-known, canonical movie (e.g. "Inception") that matches the query intent.
3) Keep lists empty when nothing is found, except 'titles' should contain either explicit titles or one recommended title as explained.
4) Keep responses short and deterministic.

Examples (these are examples for the model; they are NOT required in the response):
- "Mind-bending sci-fi movies like Inception" -> { "titles": ["Inception"], "genres": ["Science Fiction"], "keywords": ["mind-bending"] }
- "A movie where a guy forgets his memory every day and falls in love" -> { "titles": ["50 First Dates"], "keywords": ["memory loss", "romance"], "genres": ["Romance", "Comedy"] }
""")

def analyze_query(query: str) -> dict:
    prompt = PROMPT_TEMPLATE.substitute(query=query)

    # Send prompt to LLM
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    
    content = response.choices[0].message.content.strip()

    # Attempt to parse JSON
    try:
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError("Parsed content is not an object")

        # Ensure keys exist and are lists
        titles = parsed.get("titles") or []
        keywords = parsed.get("keywords") or []
        actors = parsed.get("actors") or []
        directors = parsed.get("directors") or []
        genres = parsed.get("genres") or []

        # If no titles provided, use best-effort fallback
        if not titles:
            fallback_title = keywords[0] if keywords else (query.strip() or "Unknown")
            titles = [fallback_title]

        return {
            "titles": titles,
            "keywords": keywords,
            "actors": actors,
            "directors": directors,
            "genres": genres,
        }

    except Exception as e:
        # Log raw response for debugging
        logger.warning("Failed to parse LLM response as JSON. Error: %s", e)
        logger.warning("Raw LLM content:\n%s", content)

        # Robust fallback: use raw query
        fallback = query.strip() or "Unknown"
        return {
            "titles": [fallback],
            "keywords": [fallback],
            "actors": [],
            "directors": [],
            "genres": [],
        }
