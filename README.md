# 🎬 Movie Query Engine

A full-stack movie discovery engine that lets users search for movies using **natural language** instead of just titles.

> _“A movie where a guy forgets his memory every day and falls in love”_  
> _“Mind-bending sci-fi movies like Inception”_  
> _“90s action movies with Keanu Reeves”_

The backend uses an **LLM (via Groq)** to interpret the user's intent (titles, genres, actors, mood, keywords), then calls **TMDB** to fetch relevant movies. The frontend is built with **React + Vite + Tailwind** and shows rich movie cards and detail views.

---

## 🚀 Features

- 🔍 **Natural language search** for movies (plot, mood, actors, directors, genre combos)
- 🤖 **LLM-powered intent extraction** (titles, genres, actors, keywords)
- 🎞️ **Movie cards** with poster, title, year, rating
- 📖 **Movie detail view** with full plot, genres, top cast, director, and trailer (YouTube, when available)
- ⚙️ Robust backend with:
  - TMDB integration
  - Timeouts and error handling
  - Clean structured error responses
- 🌐 CORS-enabled API for local frontend development

> **Note:** TMDB API availability depends on their service status and your local network/firewall configuration.

---

## 🧱 Tech Stack

**Frontend**

- React (Vite)
- Tailwind CSS
- Axios

**Backend**

- FastAPI
- Python `requests`
- Groq LLM client (Llama-like model)
- Pydantic for request/response models

**External APIs**

- [TMDB API](https://developer.themoviedb.org)
- [Groq](https://groq.com) for open-source LLM inference

---

## 📂 Project Structure

```bash
movie-query-engine/
│
├── backend/
│   ├── app.py                        # FastAPI entrypoint + CORS + rate limiting
│   ├── config.py                     # (optional) centralized env configuration
│   ├── services/
│   │   ├── llm_service.py            # Groq / LLM orchestration
│   │   ├── tmdb_service.py           # TMDB client + caching + normalization
│   │   └── parser_service.py         # Movie card format helper
│   ├── models/
│   │   └── schemas.py                # Request/response Pydantic models
│   ├── utils/
│   │   ├── error_handler.py          # Standardized backend error formatting
│   │   └── rate_limit.py             # Lightweight in-memory rate limiter
│   ├── requirements.txt
│   └── .env                          # Backend env vars (NOT COMMITTED)
│
└── frontend/
    ├── src/
    │   ├── App.jsx                   # UI shell using search hook
    │   ├── api.js                    # Axios instance + interceptors
    │   ├── hooks/
    │   │   └── useSearchMovies.js    # Search hook (debounced click logic)
    │   ├── components/
    │   │   ├── SearchBar.jsx
    │   │   ├── MovieCard.jsx
    │   ├── main.jsx                  # React entrypoint
    │   └── index.css                 # Tailwind base styles
    ├── vite.config.js
    ├── postcss.config.js
    ├── tailwind.config.js            # Tailwind config (generated)
    ├── package.json
    └── .env                          # Frontend env vars (NOT COMMITTED)

```

🔐 Environment Variables

```
# Backend (backend/.env)
TMDB_API_KEY=your_tmdb_v3_api_key_here
GROQ_API_KEY=your_groq_api_key_here
ENV=development
```

TMDB_API_KEY: Get this from your TMDB account → Settings → API → API Key (v3 auth).

GROQ_API_KEY: Get from Groq dashboard.
🛠️ Setup & Installation

## 1. Clone the repo
```bash
   git clone https://github.com/your-username/movie-query-engine.git
   cd movie-query-engine
```

## 2. Backend Setup (FastAPI + Python)
  ```
 Create and activate a virtual env (or use conda)
   cd backend
```

## Using venv
```
python -m venv venv
source venv/Scripts/activate # Windows
```

## or

```
source venv/bin/activate # Mac/Linux
```

## OR: using conda (if you prefer)

```
conda create -n movie-engine python=3.11
conda activate movie-engine


Install dependencies
pip install -r requirements.txt
```

## Create .env
```
TMDB_API_KEY=your_tmdb_v3_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

## Run the backend
```
uvicorn app:app --reload
```

Backend will be available at:

http://127.0.0.1:8000

Docs: http://127.0.0.1:8000/docs

## 3. Frontend Setup (React + Vite)
   Install dependencies
   ```
   cd ../frontend
   npm install
```

## Configure frontend .env
```
VITE_API_URL=http://localhost:8000/api
```

## Run the frontend
```
npm run dev
```

Open the printed URL, usually:

http://localhost:5173

# 🌐 API Endpoints
- POST /api/search
```
Description:
Takes a natural language query, uses LLM to interpret intent, and returns relevant movie matches from TMDB.

Request body:

{
"query": "90s action movies with Keanu Reeves"
}

Response:

{
"results": [
{
"id": 603,
"title": "The Matrix",
"release_year": "1999",
"rating": 8.7,
"poster": "https://image.tmdb.org/t/p/w342/....jpg"
},
...
],
"analysis": {
"titles": [],
"keywords": ["action", "90s", "Keanu Reeves"],
"actors": ["Keanu Reeves"],
"directors": [],
"genres": ["Action"]
}
}
```

## GET /api/movies/:id

Example:

GET /api/movies/603

```Response:

{
"id": 603,
"title": "The Matrix",
"overview": "...",
"genres": ["Action", "Science Fiction"],
"poster": "https://image.tmdb.org/t/p/w500/....jpg",
"trailer": "https://www.youtube.com/watch?v=...",
"cast": ["Keanu Reeves", "Carrie-Anne Moss", "..."],
"director": "Lana Wachowski"
}
```
# 🤖 LLM Prompt Design

- The backend uses an LLM (via Groq) to extract structured intent:

- Titles mentioned explicitly

- Genres inferred from description

- Actors / directors if named

- Free-form keywords (for TMDB query)

- Prompt pattern (simplified):

- You are a movie understanding engine.
```
User query: "{query}"

Extract:

- Movie titles (if any)
- Genres
- Actors/Directors
- Keywords for TMDB search

Return as JSON:
{
"titles": [],
"keywords": [],
"actors": [],
"directors": [],
"genres": []
}

```
- Then the backend uses:

titles[0] when a clear title is present

Otherwise falls back to keywords for TMDB query parameter

In a real production system you would:

Use json mode or strict formatting tools instead of eval

Add guardrails for hallucinations

# 💡 Design Decisions & Trade-offs

- FastAPI chosen for:

- Type safety via Pydantic

- Great DX and clear routing

- Easy async/await support if scaling up

- Requests (sync) over httpx for simplicity in a small take-home; can be swapped later.

- Groq/Open LLM instead of closed models to align with assignment spec.

- LLM-based intent extraction instead of building custom NLP pipeline (saves time, flexible).

- TMDB v3 API key via query param for simplicity; can upgrade to v4 Bearer+headers later.
