import React from "react";

export default function MovieModal({ movie, onClose }) {
  if (!movie) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div
        className="absolute inset-0 bg-black/60"
        onClick={onClose}
        aria-hidden="true"
      />
      <div className="relative z-10 max-w-4xl w-full mx-4 bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-50 rounded-xl shadow-xl overflow-auto max-h-[90vh]">
        <button
          onClick={onClose}
          className="absolute top-3 right-3 z-20 bg-white/10 hover:bg-white/20 rounded-full p-2"
          aria-label="Close"
        >
          ✕
        </button>

        <div className="p-6 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-1">
            <img
              src={movie.poster || "/placeholder-poster.png"}
              alt={movie.title}
              className="w-full rounded"
            />
            <div className="mt-3 text-sm text-slate-400">
              <div>
                <strong>Year:</strong> {movie.release_year || "—"}
              </div>
              <div>
                <strong>Rating:</strong> {movie.rating ?? "—"}
              </div>
              <div>
                <strong>Genres:</strong>{" "}
                {(movie.genres || []).join(", ") || "—"}
              </div>
            </div>
          </div>

          <div className="md:col-span-2">
            <h2 className="text-xl font-semibold">{movie.title}</h2>
            <p className="mt-3 text-sm text-slate-400">
              {movie.overview || "No summary available."}
            </p>

            <div className="mt-4">
              <h3 className="font-medium">Top Cast</h3>
              <p className="text-sm text-slate-300">
                {(movie.cast || []).slice(0, 10).join(", ") || "—"}
              </p>
            </div>

            <div className="mt-4">
              <h3 className="font-medium">Director</h3>
              <p className="text-sm text-slate-300">{movie.director || "—"}</p>
            </div>

            {movie.trailer && (
              <div className="mt-6">
                <h3 className="font-medium">Trailer</h3>
                <div className="mt-2 aspect-video w-full">
                  <iframe
                    title="trailer"
                    src={
                      movie.trailer.includes("youtube")
                        ? movie.trailer.replace("watch?v=", "embed/")
                        : movie.trailer
                    }
                    className="w-full h-full rounded"
                    allowFullScreen
                  />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
