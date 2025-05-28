import { useState, useEffect } from 'react';
import { useUnit } from '../context/UnitContext';

interface WeatherData {
  location: string;
  temperature: number;
  condition: string;
  humidity: number;
  windSpeed: string;
  sunrise: string;
  sunset: string;
  lastUpdated: string;
}

interface ForecastDay {
  day: string;
  high: number;
  low: number;
  condition: string;
}

interface WeatherAlert {
  type: string;
  severity: 'low' | 'medium' | 'high';
  message: string;
  time: string;
}

interface UseWeatherDataReturn {
  currentWeather: WeatherData | null;
  forecastData: ForecastDay[];
  alerts: WeatherAlert[];
  loading: boolean;
  error: string | null;
  fetchWeatherData: (location: string) => Promise<void>;
}

export const useWeatherData = (): UseWeatherDataReturn => {
  const { unit } = useUnit();
  const [currentWeather, setCurrentWeather] = useState<WeatherData | null>(null);
  const [forecastData, setForecastData] = useState<ForecastDay[]>([]);
  const [alerts, setAlerts] = useState<WeatherAlert[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchWeatherData = async (location: string) => {
    setLoading(true);
    setError(null);

    try {
      // TODO: 실제 API 호출로 대체
      // Mock data for demonstration
      await new Promise(resolve => setTimeout(resolve, 1000));

      setCurrentWeather({
        location: location,
        temperature: unit === "celsius" ? 18 : 64,
        condition: "Partly Cloudy",
        humidity: 65,
        windSpeed: "12 km/h",
        sunrise: "6:45 AM",
        sunset: "7:30 PM",
        lastUpdated: new Date().toLocaleString(),
      });

      setForecastData([
        {
          day: "Wed",
          high: unit === "celsius" ? 19 : 66,
          low: unit === "celsius" ? 13 : 55,
          condition: "Sunny",
        },
        {
          day: "Thu",
          high: unit === "celsius" ? 20 : 68,
          low: unit === "celsius" ? 14 : 57,
          condition: "Partly Cloudy",
        },
        {
          day: "Fri",
          high: unit === "celsius" ? 18 : 64,
          low: unit === "celsius" ? 12 : 54,
          condition: "Rainy",
        },
        {
          day: "Sat",
          high: unit === "celsius" ? 17 : 63,
          low: unit === "celsius" ? 11 : 52,
          condition: "Cloudy",
        },
        {
          day: "Sun",
          high: unit === "celsius" ? 21 : 70,
          low: unit === "celsius" ? 15 : 59,
          condition: "Sunny",
        },
      ]);

      setAlerts([
        {
          type: "High Temperature Warning",
          severity: "high",
          message: "Extreme heat expected during afternoon hours",
          time: "2:30 PM",
        },
        {
          type: "UV Index Alert",
          severity: "medium",
          message: "High UV levels between 10 AM and 4 PM",
          time: "10:00 AM",
        },
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch weather data");
    } finally {
      setLoading(false);
    }
  };

  // 단위가 변경될 때 데이터 업데이트
  useEffect(() => {
    if (currentWeather) {
      fetchWeatherData(currentWeather.location);
    }
  }, [unit]);

  return {
    currentWeather,
    forecastData,
    alerts,
    loading,
    error,
    fetchWeatherData,
  };
};

export type { WeatherData, ForecastDay, WeatherAlert };
