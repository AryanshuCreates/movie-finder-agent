export default function SearchBar({ value, onChange, onSearch, loading }) {
  return (
    <div className="flex gap-2 p-4">
      <input
        className="border w-full p-2 rounded bg-slate-800 text-slate-50"
        placeholder="Search movies with natural language..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
      <button
        className={`px-4 py-2 rounded ${
          loading ? "bg-slate-600 cursor-not-allowed" : "bg-blue-600"
        } text-white`}
        onClick={onSearch}
        disabled={loading}
      >
        {loading ? "Searching..." : "Search"}
      </button>
    </div>
  );
}
