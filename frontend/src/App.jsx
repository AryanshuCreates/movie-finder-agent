import { useState } from "react";
import SearchBar from "./components/SearchBar";
import MovieCard from "./components/MovieCard";
import { useSearchMovies } from "./hooks/useSearchMovies";

export default function App() {
  const [query, setQuery] = useState("");

  const { results, analysis, loading, error, searchDebounced } =
    useSearchMovies();

  const handleSearch = () => {
    if (!query.trim()) return;
    searchDebounced(query);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-50">
      <div className="max-w-5xl mx-auto py-8 px-4">
        <h1 className="text-2xl md:text-3xl font-semibold mb-4">
          🎬 Movie Query Engine
        </h1>
        <p className="text-slate-400 text-sm mb-6">
          Search using natural language – e.g.{" "}
          <span className="italic">"mind-bending sci-fi like Inception"</span>
        </p>

        <SearchBar value={query} onChange={setQuery} onSearch={handleSearch} />

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

        {loading && (
          <div className="mt-6 flex items-center gap-2 text-sm text-slate-300">
            <span className="inline-flex h-5 w-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" />
            <span>Searching movies...</span>
          </div>
        )}

        {/* Error state */}
        {error && (
          <div className="mt-4 rounded border border-red-500/40 bg-red-950/60 text-red-200 text-sm px-3 py-2">
            {error}
          </div>
        )}

        {/* Results grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
          {results.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>

        {/* Empty state */}
        {!loading && !error && query.trim() && results.length === 0 && (
          <div className="mt-6 text-sm text-slate-400">
            No movies found for this query. Try rephrasing or using actor /
            director names.
          </div>
        )}
      </div>
    </div>
  );
}
