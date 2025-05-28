interface FavoriteLocationsListProps {
  favorites: string[];
  showFavorites: boolean;
  darkMode: boolean;
  onToggleFavorites: () => void;
  onSelectLocation: (location: string) => void;
  onRemoveFavorite: (location: string) => void;
}

const FavoriteLocationsList = ({
  favorites,
  showFavorites,
  darkMode,
  onToggleFavorites,
  onSelectLocation,
  onRemoveFavorite,
}: FavoriteLocationsListProps) => {
  return (
    <div
      className={`rounded-xl shadow-lg overflow-hidden ${darkMode ? "bg-gray-800" : "bg-white"}`}
    >
      <div
        className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between cursor-pointer"
        onClick={onToggleFavorites}
      >
        <h3 className="font-semibold">Favorite Locations</h3>
        <i
          className={`fas ${showFavorites ? "fa-chevron-up" : "fa-chevron-down"} text-gray-500`}
        ></i>
      </div>
      {showFavorites && (
        <div className="p-4">
          {favorites.length > 0 ? (
            <ul className="space-y-2">
              {favorites.map((fav, index) => (
                <li
                  key={index}
                  className="flex items-center justify-between"
                >
                  <button
                    className="text-left hover:text-blue-500 cursor-pointer whitespace-nowrap !rounded-button"
                    onClick={() => onSelectLocation(fav)}
                  >
                    {fav}
                  </button>
                  <button
                    className="text-red-500 hover:text-red-600 cursor-pointer whitespace-nowrap !rounded-button"
                    onClick={() => onRemoveFavorite(fav)}
                  >
                    <i className="fas fa-times"></i>
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-gray-500 dark:text-gray-400 text-sm">
              No favorite locations saved yet.
            </p>
          )}
        </div>
      )}
    </div>
  );
};

export default FavoriteLocationsList;
