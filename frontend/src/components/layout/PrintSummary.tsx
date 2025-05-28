import React, { FC } from 'react';
import { WeatherData, ForecastDay } from '../../hooks/useWeatherData';

interface PrintSummaryProps {
  currentWeather: WeatherData;
  forecastData: ForecastDay[];
  unit: 'celsius' | 'fahrenheit';
}

const PrintSummary: FC<PrintSummaryProps> = ({
  currentWeather,
  forecastData,
  unit,
}) => {
  return (
    <div className="hidden print:block p-8">
      <h1 className="text-3xl font-bold mb-6">
        Weather Report - {currentWeather.location}
      </h1>
      <div className="mb-6">
        <p className="text-lg">Generated on: {new Date().toLocaleString()}</p>
        <p className="text-lg">
          Current Temperature: {currentWeather.temperature}°
          {unit === "celsius" ? "C" : "F"}
        </p>
        <p className="text-lg">Condition: {currentWeather.condition}</p>
      </div>
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div>
          <h2 className="text-xl font-semibold mb-2">Current Conditions</h2>
          <p>Humidity: {currentWeather.humidity}%</p>
          <p>Wind Speed: {currentWeather.windSpeed}</p>
          <p>Sunrise: {currentWeather.sunrise}</p>
          <p>Sunset: {currentWeather.sunset}</p>
        </div>
        <div>
          <h2 className="text-xl font-semibold mb-2">5-Day Forecast</h2>
          {forecastData.map((day, index) => (
            <p key={index}>
              {day.day}: {day.high}° / {day.low}° - {day.condition}
            </p>
          ))}
        </div>
      </div>
      <div className="text-sm text-gray-500">
        <p>Weather Dashboard - https://weather.app</p>
        <p>Report generated for: {currentWeather.location}</p>
      </div>
    </div>
  );
};

export default PrintSummary; 