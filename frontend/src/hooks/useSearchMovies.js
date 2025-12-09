import { useState, useMemo } from "react";
import api from "../api";
import debounce from "lodash.debounce";

export function useSearchMovies() {
  const [results, setResults] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const searchNow = async (query) => {
    if (!query.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const { data } = await api.post("/search", { query });
      setResults(data.results || []);
      setAnalysis(data.analysis || null);
    } catch (err) {
      setError(err.message || "Failed to search movies");
    } finally {
      setLoading(false);
    }
  };

  const searchDebounced = useMemo(() => debounce(searchNow, 500), []);

  return { results, analysis, loading, error, searchNow, searchDebounced };
}
