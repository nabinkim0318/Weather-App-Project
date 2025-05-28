import React, { FC } from 'react';
import CurrentWeather from '../CurrentWeather';
import ForecastList from '../ForecastList';
import HourlyForecast from '../HourlyForecast';
import GoogleMap from '../GoogleMap';
import FavoriteLocationsList from '../FavoriteLocationsList';
import WeatherAlerts from '../WeatherAlerts';
import ExportButtons from '../ExportButtons';
import ShareButtons from '../ShareButtons';
import YouTubeVideos from '../YouTubeVideos';
import { WeatherData, ForecastDay, WeatherAlert } from '../../hooks/useWeatherData';

interface MainContentProps {
  currentWeather: WeatherData;
  forecastData: ForecastDay[];
  alerts: WeatherAlert[];
  unit: 'celsius' | 'fahrenheit';
  darkMode: boolean;
  favorites: string[];
  showFavorites: boolean;
  onAddToFavorites: () => void;
  onToggleFavorites: () => void;
  onSelectLocation: (location: string) => void;
  onRemoveFavorite: (location: string) => void;
  onExport: (format: 'csv' | 'json') => void;
}

const MainContent: FC<MainContentProps> = ({
  currentWeather,
  forecastData,
  alerts,
  unit,
  darkMode,
  favorites,
  showFavorites,
  onAddToFavorites,
  onToggleFavorites,
  onSelectLocation,
  onRemoveFavorite,
  onExport,
}) => {
  return (
    <>
      <main className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <CurrentWeather
          currentWeather={currentWeather}
          unit={unit}
          darkMode={darkMode}
          onAddToFavorites={onAddToFavorites}
        />
        <div className="space-y-6">
          <GoogleMap location={currentWeather.location} darkMode={darkMode} />
          <FavoriteLocationsList
            favorites={favorites}
            showFavorites={showFavorites}
            darkMode={darkMode}
            onToggleFavorites={onToggleFavorites}
            onSelectLocation={onSelectLocation}
            onRemoveFavorite={onRemoveFavorite}
          />
          <WeatherAlerts alerts={alerts} darkMode={darkMode} />
          <div
            className={`rounded-xl shadow-lg overflow-hidden ${
              darkMode ? "bg-gray-800" : "bg-white"
            }`}
          >
            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 className="font-semibold">Export & Share</h3>
            </div>
            <div className="p-4 flex flex-wrap items-center gap-6">
              <ExportButtons onExport={onExport} />
              <div className="h-8 w-px bg-gray-300 dark:bg-gray-600"></div>
              <ShareButtons
                location={currentWeather.location}
                temperature={currentWeather.temperature}
                condition={currentWeather.condition}
                unit={unit}
              />
            </div>
          </div>
        </div>
      </main>

      <div className="mt-8">
        <ForecastList forecastData={forecastData} darkMode={darkMode} />
        <HourlyForecast unit={unit} darkMode={darkMode} />
        <YouTubeVideos location={currentWeather.location} darkMode={darkMode} />
      </div>
    </>
  );
};

export default MainContent; 