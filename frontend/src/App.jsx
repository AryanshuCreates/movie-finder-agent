// frontend/src/App.jsx
import { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import MovieCard from "./components/MovieCard";
import MovieModal from "./components/MovieModal";
import { useSearchMovies } from "./hooks/useSearchMovies";
import api from "./api";

export default function App() {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState(null); // movie details (object)
  const [detailLoading, setDetailLoading] = useState(false);
  const [detailError, setDetailError] = useState(null);

  const {
    results,
    analysis,
    loading, // search loading
    error, // search error
    searchNow, // immediate search (if you want to use)
    searchDebounced,
  } = useSearchMovies();

  // Make sure we cancel any pending debounced calls on unmount
  useEffect(() => {
    return () => {
      // lodash.debounce exposes .cancel()
      searchDebounced.cancel?.();
    };
  }, [searchDebounced]);

  const handleSearch = () => {
    if (!query.trim()) return;
    // Debounce only the explicit search click
    searchDebounced(query);
  };

  const openDetails = async (movie) => {
    setDetailError(null);
    setDetailLoading(true);
    setSelected(null); // clear previous while loading
    try {
      const { data } = await api.get(`/movies/${movie.id}`);
      setSelected(data);
    } catch (err) {
      console.error("Failed to fetch details", err);
      setDetailError("Failed to load movie details. Try again.");
    } finally {
      setDetailLoading(false);
    }
  };

  const closeDetails = () => {
    setSelected(null);
    setDetailError(null);
    setDetailLoading(false);
  };

  return (
    <div className="min-h-screen w-full bg-slate-950 text-slate-50">
      <div className="max-w-5xl mx-auto py-8 px-4">
        <h1 className="text-2xl md:text-3xl font-semibold mb-4 text-center">
          🎬 Movie Query Engine
        </h1>
        <p className="text-slate-400 text-sm mb-6">
          Search using natural language — it can be a plot, mood, genre combo,
          or partial scene. Example:{" "}
          <span className="italic">"Mind-bending sci-fi like Inception"</span>
        </p>

        <SearchBar
          value={query}
          onChange={setQuery}
          onSearch={handleSearch}
          loading={loading}
        />

        {analysis && (
          <div className="mt-4 text-xs text-slate-400 space-y-1">
            <div className="font-semibold text-slate-300">
              LLM understanding of your query:
            </div>
            {analysis.titles?.length > 0 && (
              <div>
                <span className="font-medium">Titles:</span>{" "}
                {analysis.titles.join(", ")}
              </div>
            )}
            {analysis.genres?.length > 0 && (
              <div>
                <span className="font-medium">Genres:</span>{" "}
                {analysis.genres.join(", ")}
              </div>
            )}
            {analysis.actors?.length > 0 && (
              <div>
                <span className="font-medium">Actors:</span>{" "}
                {analysis.actors.join(", ")}
              </div>
            )}
            {analysis.directors?.length > 0 && (
              <div>
                <span className="font-medium">Directors:</span>{" "}
                {analysis.directors.join(", ")}
              </div>
            )}
          </div>
        )}

        {/* Search loader */}
        {loading && (
          <div className="mt-6 flex items-center gap-2 text-sm text-slate-300">
            <span className="inline-flex h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <span>Searching movies...</span>
          </div>
        )}

        {/* Search error */}
        {error && (
          <div className="mt-4 rounded border border-red-500/40 bg-red-950/60 text-red-200 text-sm px-3 py-2">
            {typeof error === "string"
              ? error
              : error?.message ?? "Something went wrong"}
          </div>
        )}

        {/* Results grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          {results.map((movie) => (
            <MovieCard
              key={movie.id}
              movie={movie}
              onClick={() => openDetails(movie)}
            />
          ))}
        </div>

        {/* Empty state */}
        {!loading && !error && query.trim() && results.length === 0 && (
          <div className="mt-6 text-sm text-slate-400">
            No movies found for this query. Try rephrasing, using actor/director
            names, or a different mood.
          </div>
        )}
      </div>

      {/* Modal & detail states */}
      {detailLoading && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div className="absolute inset-0 bg-black/60" />
          <div className="relative z-10 bg-slate-900 text-slate-50 rounded-lg p-6 shadow-lg">
            <div className="flex items-center gap-3">
              <span className="inline-flex h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
              <span>Loading details...</span>
            </div>
          </div>
        </div>
      )}

      {detailError && (
        <div className="fixed left-1/2 -translate-x-1/2 bottom-8 z-50">
          <div className="rounded border border-red-500/40 bg-red-950/60 text-red-200 text-sm px-4 py-2">
            {detailError}
          </div>
        </div>
      )}

      {selected && <MovieModal movie={selected} onClose={closeDetails} />}
    </div>
  );
}
