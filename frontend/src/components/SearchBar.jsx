export default function SearchBar({ value, onChange, onSearch }) {
  return (
    <div className="flex gap-2 p-4">
      <input
        className="border w-full p-2 rounded"
        placeholder="Search movies with natural language..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded"
        onClick={onSearch}
      >
        Search
      </button>
    </div>
  );
}
