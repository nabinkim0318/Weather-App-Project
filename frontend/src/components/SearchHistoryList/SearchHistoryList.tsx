interface SearchHistoryListProps {
  searchResults: string[];
  showSearchResults: boolean;
  onLocationSelect: (location: string) => void;
}

const SearchHistoryList = ({
  searchResults,
  showSearchResults,
  onLocationSelect,
}: SearchHistoryListProps) => {
  if (!showSearchResults || searchResults.length === 0) return null;

  return (
    <ul className="absolute z-10 w-full bg-white dark:bg-gray-800 mt-1 rounded-lg shadow-lg">
      {searchResults.map((result, index) => (
        <li key={index}>
          <button
            className="w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700"
            onClick={() => onLocationSelect(result)}
          >
            <i className="fas fa-map-marker-alt mr-2 text-gray-500"></i>
            {result}
          </button>
        </li>
      ))}
    </ul>
  );
};

export default SearchHistoryList;
