import { useState } from "react";
import api from "./api";
import SearchBar from "./components/SearchBar";
import MovieCard from "./components/MovieCard";

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const performSearch = async () => {
    const { data } = await api.post("/search", { query });
    setResults(data.results);
  };

  return (
    <div className="p-6">
      <SearchBar value={query} onChange={setQuery} onSearch={performSearch} />
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
        {results.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    </div>
  );
}
