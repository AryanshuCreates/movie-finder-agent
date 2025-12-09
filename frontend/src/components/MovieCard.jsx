export default function MovieCard({ movie, onClick }) {
  const poster = movie.poster || "/placeholder-poster.png";
  const year =
    movie.release_year ||
    (movie.release_date && movie.release_date.slice(0, 4)) ||
    "—";
  const rating = movie.rating ?? movie.vote_average ?? "—";

  return (
    <div
      className="bg-white/5 hover:bg-white/6 shadow-sm rounded-lg hover:scale-105 cursor-pointer transition p-2 flex flex-col"
      onClick={onClick}
      role="button"
      tabIndex={0}
    >
      <div className="aspect-[2/3] w-full overflow-hidden rounded">
        <img
          src={poster}
          alt={movie.title}
          className="w-full h-full object-cover"
        />
      </div>

      <div className="mt-3">
        <h3 className="font-semibold text-sm">{movie.title}</h3>
        <div className="text-xs text-slate-300 mt-1 flex items-center justify-between">
          <span>{year}</span>
          <span className="bg-slate-800/40 px-2 py-0.5 rounded text-xs">
            {rating !== "—" ? `⭐ ${rating}` : "—"}
          </span>
        </div>
      </div>
    </div>
  );
}
