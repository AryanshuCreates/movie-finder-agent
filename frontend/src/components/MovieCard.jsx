export default function MovieCard({ movie, onClick }) {
  return (
    <div
      className="bg-white shadow rounded hover:scale-105 cursor-pointer transition p-2"
      onClick={onClick}
    >
      <img src={movie.poster} alt="" className="rounded" />
      <h3 className="font-bold mt-2">{movie.title}</h3>
      <p className="text-gray-500">{movie.release_year}</p>
    </div>
  );
}
