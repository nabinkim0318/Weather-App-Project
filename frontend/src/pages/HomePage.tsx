import React, { useState, type FC } from 'react';
import { useTheme } from '../context/ThemeContext';
import { useUnit } from '../context/UnitContext';
import { useUser } from '../context/UserContext';
import { useWeatherData } from '../hooks/useWeatherData';
import { useGeolocation } from '../hooks/useGeolocation';
import Header from '../components/layout/Header';
import MainContent from '../components/layout/MainContent';
import PrintSummary from '../components/layout/PrintSummary';
import Footer from '../components/layout/Footer';
import LoadingSpinner from '../components/LoadingSpinner';

const HomePage: FC = () => {
  const { darkMode, toggleTheme } = useTheme();
  const { unit, toggleUnit } = useUnit();
  const { preferences, addToFavorites, removeFromFavorites, addToRecentSearches } = useUser();
  const { currentWeather, forecastData, alerts, loading, error, fetchWeatherData } = useWeatherData();
  const { getCurrentPosition, loading: locationLoading, error: locationError } = useGeolocation();

  const [location, setLocation] = useState<string>("");
  const [searchResults, setSearchResults] = useState<string[]>([]);
  const [showSearchResults, setShowSearchResults] = useState<boolean>(false);
  const [showFavorites, setShowFavorites] = useState<boolean>(false);

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setLocation(value);
    if (value.length > 2) {
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

  const handleLocationSelect = async (selectedLocation: string) => {
    setLocation(selectedLocation);
    addToRecentSearches(selectedLocation);
    await fetchWeatherData(selectedLocation);
  };

  const handleUseMyLocation = async () => {
    const position = await getCurrentPosition();
    if (position) {
      const mockLocationName = "San Francisco, CA";
      setLocation(mockLocationName);
      await fetchWeatherData(mockLocationName);
    }
  };

  const toggleFavorites = () => {
    setShowFavorites(!showFavorites);
  };

  const exportData = (format: "csv" | "json") => {
    if (!currentWeather) return;

    const data = {
      current: currentWeather,
      forecast: forecastData,
    };

    if (format === "json") {
      const jsonString = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonString], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `weather_data_${new Date().toISOString().split("T")[0]}.json`;
      a.click();
    } else {
      let csv = "Day,High,Low,Condition\n";
      forecastData.forEach((day) => {
        csv += `${day.day},${day.high},${day.low},${day.condition}\n`;
      });
      const blob = new Blob([csv], { type: "text/csv" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `weather_forecast_${new Date().toISOString().split("T")[0]}.csv`;
      a.click();
    }
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-800'}`}>
      {(loading || locationLoading) && <LoadingSpinner />}
      <div className="max-w-7xl mx-auto px-4 py-6">
        <Header
          darkMode={darkMode}
          unit={unit}
          onLocationSelect={handleLocationSelect}
          onUseMyLocation={handleUseMyLocation}
          toggleUnit={toggleUnit}
          toggleTheme={toggleTheme}
          error={error}
          locationError={locationError}
        />

        {currentWeather && (
          <>
            <MainContent
              currentWeather={currentWeather}
              forecastData={forecastData}
              alerts={alerts}
              unit={unit}
              darkMode={darkMode}
              favorites={preferences.favorites}
              showFavorites={showFavorites}
              onAddToFavorites={() => addToFavorites(currentWeather.location)}
              onToggleFavorites={toggleFavorites}
              onSelectLocation={handleLocationSelect}
              onRemoveFavorite={removeFromFavorites}
              onExport={exportData}
            />

            <PrintSummary
              currentWeather={currentWeather}
              forecastData={forecastData}
              unit={unit}
            />
          </>
        )}
      </div>

      <Footer darkMode={darkMode} />
    </div>
  );
};

export default HomePage;
