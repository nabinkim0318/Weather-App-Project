import { useState, type ChangeEvent } from 'react';
import UseMyLocationButton from '../UseMyLocationButton';

interface LocationSearchProps {
  onLocationSelect: (location: string) => void;
  onUseMyLocation: () => void;
  darkMode: boolean;
}

const LocationSearch = ({ onLocationSelect, onUseMyLocation, darkMode }: LocationSearchProps) => {
  const [location, setLocation] = useState<string>('');
  const [searchResults, setSearchResults] = useState<string[]>([]);
  const [showSearchResults, setShowSearchResults] = useState<boolean>(false);

  const handleSearch = (e: ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setLocation(value);
    
    if (value.length > 2) {
      // Mock search results
      setSearchResults([
        "San Francisco, CA",
        "San Diego, CA",
        "San Jose, CA",
        "Santa Barbara, CA",
      ]);
      setShowSearchResults(true);
    } else {
      setSearchResults([]);
      setShowSearchResults(false);
    }
  };

  const handleSelectLocation = (location: string) => {
    setLocation(location);
    setShowSearchResults(false);
    onLocationSelect(location);
  };

  return (
    <div className="relative w-full md:w-80">
      <div className="relative">
        <input
          type="text"
          placeholder="Search location..."
          value={location}
          onChange={handleSearch}
          className={`w-full pl-10 pr-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            darkMode
              ? "bg-gray-800 text-white border-gray-700"
              : "bg-white text-gray-800 border-gray-300"
          } border`}
        />
        <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
          <i className="fas fa-search"></i>
        </span>
      </div>

      {showSearchResults && searchResults.length > 0 && (
        <div
          className={`absolute z-10 w-full mt-1 rounded-lg shadow-lg ${
            darkMode
              ? "bg-gray-800 border-gray-700"
              : "bg-white border-gray-200"
          } border`}
        >
          <ul>
            {searchResults.map((result, index) => (
              <li
                key={index}
                className={`px-4 py-2 cursor-pointer hover:bg-blue-100 hover:text-blue-800 ${
                  darkMode ? "hover:bg-gray-700 hover:text-blue-300" : ""
                }`}
                onClick={() => handleSelectLocation(result)}
              >
                {result}
              </li>
            ))}
          </ul>
        </div>
      )}

      <UseMyLocationButton onUseMyLocation={onUseMyLocation} className="ml-2" />
    </div>
  );
};

export default LocationSearch;
