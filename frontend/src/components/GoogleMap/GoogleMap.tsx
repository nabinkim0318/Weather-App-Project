interface GoogleMapProps {
  location: string;
  darkMode: boolean;
}

const GoogleMap = ({ location, darkMode }: GoogleMapProps) => {
  return (
    <div
      className={`rounded-xl shadow-lg overflow-hidden ${darkMode ? "bg-gray-800" : "bg-white"}`}
    >
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h3 className="font-semibold">Location Map</h3>
      </div>
      <div className="h-64 bg-gray-300 dark:bg-gray-700 relative overflow-hidden">
        <img
          src={`https://readdy.ai/api/search-image?query=A%20detailed%20satellite%20map%20view%20of%20${encodeURIComponent(location)}%20showing%20the%20downtown%20area%20with%20clear%20geographical%20features%20and%20landmarks%2C%20high%20resolution%20satellite%20imagery&width=600&height=300&seq=1&orientation=landscape`}
          alt={`Map of ${location}`}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="bg-blue-500 h-6 w-6 rounded-full flex items-center justify-center">
            <div className="bg-white h-2 w-2 rounded-full"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GoogleMap;
