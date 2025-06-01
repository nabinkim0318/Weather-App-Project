import React, { useState, useEffect } from 'react';
import * as echarts from 'echarts';
import type { EChartsOption } from 'echarts';

// API Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface YouTubeVideo {
    videoId: string;
    title: string;
    description: string;
    thumbnail: string;
    embed_url: string;
    watch_url: string;
    category: string;
}

interface MapData {
    embed_url: string;
}

interface WeatherData {
    name: string;
    main: {
        temp: number;
        humidity: number;
    };
    weather: Array<{
        main: string;
        description: string;
    }>;
    wind: {
        speed: number;
    };
    sys: {
        sunrise: number;
        sunset: number;
    };
}

interface LocationSearchResult {
    name: string;
    country: string;
    state?: string;
}

interface ForecastItem {
    forecast_date: string;
    forecast_hour: number;
    temp_c: number;
    temp_f: number;
    condition: string;
    condition_desc: string;
    icon: string;
    icon_url: string;
}

interface ForecastData {
    location: {
        city: string;
        country: string;
        latitude: number;
        longitude: number;
    };
    forecast: ForecastItem[];
}

// Add new interface for hourly weather data
interface HourlyWeather {
    hour: string;
    timestamp: number;
    temperature: number;
    condition: string;
    description: string;
    icon: string;
}

interface HourlyWeatherResponse {
    location: string;
    hourly_forecast: HourlyWeather[];
}

// Weather History interface
interface WeatherHistoryRecord {
    id: number;
    location: string;
    date: string;
    temperature: number;
    condition: string;
    humidity: number;
    wind_speed: number;
    created_at: string;
}

interface WeatherHistorySearch {
    location: string;
    startDate: string;
    endDate: string;
}

function App(): React.ReactElement {
    const [loading, setLoading] = useState<boolean>(false);
    const [location, setLocation] = useState<string>('');
    const [searchResults, setSearchResults] = useState<LocationSearchResult[]>([]);
    const [showSearchResults, setShowSearchResults] = useState<boolean>(false);
    const [unit, setUnit] = useState<'celsius' | 'fahrenheit'>('fahrenheit');
    const [darkMode, setDarkMode] = useState<boolean>(false);
    const [showFavorites, setShowFavorites] = useState<boolean>(false);
    const [favorites, setFavorites] = useState<string[]>(['London', 'New York', 'Tokyo']);
    const [error, setError] = useState<string | null>(null);
    const [videos, setVideos] = useState<YouTubeVideo[]>([]);
    const [videoError, setVideoError] = useState<string | null>(null);
    const [mapUrl, setMapUrl] = useState<string>('');
    const [mapError, setMapError] = useState<string | null>(null);
    const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
    const [weatherError, setWeatherError] = useState<string | null>(null);
    const [forecastData, setForecastData] = useState<ForecastData | null>(null);
    const [forecastError, setForecastError] = useState<string | null>(null);
    const [hourlyData, setHourlyData] = useState<HourlyWeatherResponse | null>(null);
    const [isAddingFavorite, setIsAddingFavorite] = useState<boolean>(false);
    // Weather History related state
    const [historySearch, setHistorySearch] = useState<WeatherHistorySearch>({
        location: '',
        startDate: '',
        endDate: ''
    });
    const [historyRecords, setHistoryRecords] = useState<WeatherHistoryRecord[]>([]);
    const [isHistoryLoading, setIsHistoryLoading] = useState<boolean>(false);
    const [historyError, setHistoryError] = useState<string | null>(null);

    // Initial load: fetch weather for Washington DC
    useEffect(() => {
        handleSelectLocation('Washington DC', true);
    }, []); // Run only once on component mount
    // Mock weather data
    const currentWeather = {
        location: 'San Francisco',
        temperature: unit === 'celsius' ? 18 : 64,
        condition: 'Partly Cloudy',
        humidity: 65,
        windSpeed: '12 km/h',
        sunrise: '6:45 AM',
        sunset: '7:30 PM',
        lastUpdated: 'May 27, 2025 10:30 AM'
    };
    const mockForecastData = [
        { day: 'Wed', high: unit === 'celsius' ? 19 : 66, low: unit === 'celsius' ? 13 : 55, condition: 'Sunny' },
        { day: 'Thu', high: unit === 'celsius' ? 20 : 68, low: unit === 'celsius' ? 14 : 57, condition: 'Partly Cloudy' },
        { day: 'Fri', high: unit === 'celsius' ? 18 : 64, low: unit === 'celsius' ? 12 : 54, condition: 'Rainy' },
        { day: 'Sat', high: unit === 'celsius' ? 17 : 63, low: unit === 'celsius' ? 11 : 52, condition: 'Cloudy' },
        { day: 'Sun', high: unit === 'celsius' ? 21 : 70, low: unit === 'celsius' ? 15 : 59, condition: 'Sunny' }
    ];
    const handleSearch = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const value = e.target.value;
        setLocation(value);
        
        // Only run auto-complete search if input is 3+ characters
        if (value.length > 2) {
            try {
                const response = await fetch(`${API_BASE_URL}/api/location/search`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: value, limit: 5 })
                });
                
                if (!response.ok) {
                    throw new Error('Failed to fetch locations');
                }
                
                const data: LocationSearchResult[] = await response.json();
                setSearchResults(data);
                setShowSearchResults(true);
            } catch (error) {
                console.error('Error searching locations:', error);
                setSearchResults([]);
            }
        } else {
            setSearchResults([]);
            setShowSearchResults(false);
        }
    };
    const handleSelectLocation = async (location: string, isInitialLoad: boolean = false) => {
        // Validate empty input (only check for non-initial load)
        if (!isInitialLoad && (!location || location.trim() === '')) {
            setError('Please enter a location: city name (Seoul), zip code (10001), coordinates (37.5665,126.978), or landmark (Times Square)');
            return;
        }

        try {
            setLoading(true);
            setError(null); // Clear existing error
            if (!isInitialLoad) {
                setLocation(location);
            }
            setShowSearchResults(false);

            await Promise.all([
                fetch(`${API_BASE_URL}/api/location/weather?user_input=${encodeURIComponent(location)}`).then(async (response) => {
                    if (!response.ok) {
                        // 400 error (invalid zip code, etc.)
                        if (response.status === 400) {
                            const errorData = await response.json();
                            throw new Error(`INVALID_INPUT:${errorData.detail}`);
                        }
                        throw new Error('Failed to fetch weather data');
                    }
                    const data = await response.json();
                    setWeatherData(data);
                    return data;
                }),
                fetch(`${API_BASE_URL}/api/weather/forecast?city=${encodeURIComponent(location)}`).then(async (response) => {
                    if (!response.ok) {
                        // forecast API only supports city, so ignore zip code errors
                        if (response.status === 400) {
                            return null; // proceed without forecast data
                        }
                        throw new Error('Failed to fetch forecast data');
                    }
                    const data = await response.json();
                    setForecastData(data);
                    return data;
                }),
                fetchHourlyWeather(location)
            ]);
        } catch (error) {
            console.error('Error fetching weather data:', error);
            
            // Handle error messages
            const errorMessage = error instanceof Error ? error.message : 'Failed to fetch weather data';
            
            // Check if it's a zip code related error
            if (errorMessage.startsWith('INVALID_INPUT:')) {
                const actualError = errorMessage.replace('INVALID_INPUT:', '');
                setError(actualError);
            } else {
                setError(errorMessage);
            }
        } finally {
            setLoading(false);
        }
    };
    const handleUseMyLocation = () => {
        if (!navigator.geolocation) {
            setError('Browser does not support location information');
            return;
        }

        setLoading(true);
        setError(null);
        setWeatherData(null);
        setForecastData(null);

        navigator.geolocation.getCurrentPosition(
            // Success callback
            async (position) => {
                try {
                    const { latitude, longitude } = position.coords;
                    console.log('Current location:', { latitude, longitude });

                    // Get weather and forecast data in parallel
                    const [weatherResponse, forecastResponse] = await Promise.all([
                        fetch(`${API_BASE_URL}/api/location/weather?user_input=${latitude},${longitude}`),
                        fetch(`${API_BASE_URL}/api/weather/forecast?lat=${latitude}&lon=${longitude}`)
                    ]);

                    console.log('Weather API Response:', {
                        status: weatherResponse.status,
                        statusText: weatherResponse.statusText
                    });
                    console.log('Forecast API Response:', {
                        status: forecastResponse.status,
                        statusText: forecastResponse.statusText
                    });

                    // Check weather response
                    if (!weatherResponse.ok) {
                        const errorText = await weatherResponse.text();
                        console.error('Weather API Error:', errorText);
                        throw new Error(`Weather API error: ${weatherResponse.status} - ${errorText}`);
                    }
                    const weatherData = await weatherResponse.json();
                    console.log('Weather Data:', weatherData);
                    setWeatherData(weatherData);
                    setLocation(weatherData.name); // Update location name

                    // Check forecast response
                    if (!forecastResponse.ok) {
                        const errorText = await forecastResponse.text();
                        console.error('Forecast API Error:', errorText);
                        throw new Error(`Forecast API error: ${forecastResponse.status} - ${errorText}`);
                    }
                    const forecastData = await forecastResponse.json();
                    console.log('Forecast Data:', forecastData);
                    setForecastData(forecastData);

                } catch (error) {
                    console.error('Error fetching weather data:', error);
                    setError(error instanceof Error ? error.message : 'Failed to fetch weather data for your location');
                } finally {
                    setLoading(false);
                }
            },
            // Error callback
            (error) => {
                console.error('Geolocation error:', error);
                let errorMessage = 'Failed to get your location';
                
                // Provide more specific error messages
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        errorMessage = 'Please allow location access to use this feature';
                        break;
                    case error.POSITION_UNAVAILABLE:
                        errorMessage = 'Location information is unavailable';
                        break;
                    case error.TIMEOUT:
                        errorMessage = 'Location request timed out';
                        break;
                }
                
                setError(errorMessage);
                setLoading(false);
            },
            // Options
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    };
    const toggleUnit = () => {
        setUnit(unit === 'celsius' ? 'fahrenheit' : 'celsius');
    };
    const toggleTheme = () => {
        setDarkMode(!darkMode);
    };
    const toggleFavorites = () => {
        setShowFavorites(!showFavorites);
    };
    const toggleFavorite = () => {
        if (!weatherData?.name) return;
        
        const locationName = weatherData.name;
        const isFavorite = favorites.includes(locationName);
        
        if (isFavorite) {
            // Remove from favorites
            setFavorites(favorites.filter(fav => fav !== locationName));
        } else {
            // Add to favorites
            setIsAddingFavorite(true);
            setFavorites([...favorites, locationName]);
            
            // 1.2 seconds delay
            setTimeout(() => {
                setIsAddingFavorite(false);
            }, 1200);
        }
    };
    const removeFavorite = (location: string) => {
        setFavorites(favorites.filter(fav => fav !== location));
    };
    const exportData = (format: 'csv' | 'json') => {
        const data = {
            current_weather: weatherData ? {
                location: weatherData.name,
                temperature: convertTemperature(weatherData.main.temp),
                unit: unit === 'celsius' ? '°C' : '°F',
                condition: weatherData.weather[0].main,
                description: weatherData.weather[0].description,
                humidity: weatherData.main.humidity,
                wind_speed: weatherData.wind.speed,
                sunrise: weatherData.sys?.sunrise ? new Date(weatherData.sys.sunrise * 1000).toLocaleTimeString() : 'N/A',
                sunset: weatherData.sys?.sunset ? new Date(weatherData.sys.sunset * 1000).toLocaleTimeString() : 'N/A'
            } : null,
            hourly_forecast: hourlyData ? hourlyData.hourly_forecast.map(item => ({
                hour: item.hour,
                temperature: unit === 'celsius' ? item.temperature : (item.temperature * 9/5) + 32,
                unit: unit === 'celsius' ? '°C' : '°F',
                condition: item.condition,
                description: item.description
            })) : [],
            daily_forecast: forecastData ? forecastData.forecast.reduce((acc, item) => {
                const date = item.forecast_date;
                if (!acc[date]) {
                    acc[date] = {
                        date: new Date(date).toLocaleDateString(),
                        temperature_high: unit === 'celsius' ? item.temp_c : item.temp_f,
                        temperature_low: unit === 'celsius' ? item.temp_c - 5 : item.temp_f - 9,
                        unit: unit === 'celsius' ? '°C' : '°F',
                        condition: item.condition,
                        description: item.condition_desc
                    };
                }
                return acc;
            }, {} as Record<string, any>) : {}
        };

        if (format === 'json') {
            const jsonString = JSON.stringify(data, null, 2);
            const blob = new Blob([jsonString], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `weather_data_${new Date().toISOString().split('T')[0]}.json`;
            a.click();
        } else {
            let csv = 'Weather Report\n\n';
            
            // Current Weather
            if (data.current_weather) {
                csv += 'Current Weather\n';
                csv += `Location,${data.current_weather.location}\n`;
                csv += `Temperature,${data.current_weather.temperature}${data.current_weather.unit}\n`;
                csv += `Condition,${data.current_weather.condition}\n`;
                csv += `Description,${data.current_weather.description}\n`;
                csv += `Humidity,${data.current_weather.humidity}%\n`;
                csv += `Wind Speed,${data.current_weather.wind_speed} m/s\n`;
                csv += `Sunrise,${data.current_weather.sunrise}\n`;
                csv += `Sunset,${data.current_weather.sunset}\n\n`;
            }

            // Hourly Forecast
            if (data.hourly_forecast.length > 0) {
                csv += 'Hourly Forecast\n';
                csv += 'Hour,Temperature,Condition,Description\n';
                data.hourly_forecast.forEach(item => {
                    csv += `${item.hour},${item.temperature}${item.unit},${item.condition},${item.description}\n`;
                });
                csv += '\n';
            }

            // Daily Forecast
            if (Object.keys(data.daily_forecast).length > 0) {
                csv += '5-Day Forecast\n';
                csv += 'Date,High,Low,Condition,Description\n';
                Object.values(data.daily_forecast).forEach(item => {
                    csv += `${item.date},${item.temperature_high}${item.unit},${item.temperature_low}${item.unit},${item.condition},${item.description}\n`;
                });
            }

            const blob = new Blob([csv], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `weather_report_${new Date().toISOString().split('T')[0]}.csv`;
            a.click();
        }
    };
    // Get YouTube Videos
    const fetchYouTubeVideos = async (city: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/integrations/youtube?city=${encodeURIComponent(city)}`);
            if (!response.ok) {
                throw new Error('Failed to fetch videos');
            }
            const data = await response.json();
            setVideos(data);
            setVideoError(null);
        } catch (error) {
            console.error('Error fetching videos:', error);
            setVideoError('Failed to fetch videos');
            setVideos([]);
        }
    };
    // Update Videos when location changes
    useEffect(() => {
        if (weatherData?.name) {
            fetchYouTubeVideos(weatherData.name);
        }
    }, [weatherData?.name]);
    // Get Map Data
    const fetchMapData = async (city: string, lat?: number, lon?: number) => {
        try {
            let url = `${API_BASE_URL}/api/integrations/map`;
            if (lat && lon) {
                url += `?lat=${lat}&lon=${lon}`;
            } else {
                url += `?city=${encodeURIComponent(city)}`;
            }
            
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Failed to fetch map data');
            }
            const data: MapData = await response.json();
            setMapUrl(data.embed_url);
            setMapError(null);
        } catch (error) {
            console.error('Error fetching map:', error);
            setMapError('Failed to fetch map');
            setMapUrl('');
        }
    };
    // Update Map when location changes
    useEffect(() => {
        if (weatherData?.name) {
            // Use latitude/longitude from weather data if available
            if (forecastData?.location?.latitude && forecastData?.location?.longitude) {
                fetchMapData(
                    weatherData.name,
                    forecastData.location.latitude,
                    forecastData.location.longitude
                );
            } else {
                fetchMapData(weatherData.name);
            }
        }
    }, [weatherData?.name, forecastData?.location]);
    // Add fetchHourlyWeather function
    const fetchHourlyWeather = async (location: string) => {
        try {
            const response = await fetch(`${API_BASE_URL}/api/weather/hourly?city=${encodeURIComponent(location)}`);
            if (!response.ok) {
                throw new Error('Failed to fetch hourly weather data');
            }
            const data = await response.json();
            setHourlyData(data);
        } catch (error) {
            console.error('Error fetching hourly weather:', error);
        }
    };
    // Modify useEffect for chart to use hourly data
    useEffect(() => {
        const chartDom = document.getElementById('temperature-chart');
        if (!chartDom) return;

        echarts.dispose(chartDom);
        const myChart = echarts.init(chartDom as HTMLDivElement);

        const hours = hourlyData?.hourly_forecast.map(item => item.hour) || [];
        const temperatures = hourlyData?.hourly_forecast.map(item => 
            unit === 'celsius' ? item.temperature : (item.temperature * 9/5) + 32
        ) || [];

        myChart.setOption({
            animation: false,
            backgroundColor: darkMode ? '#1f2937' : '#ffffff',
            tooltip: {
                trigger: 'axis',
                formatter: function (params: any) {
                    return `${params[0].name}: ${params[0].value.toFixed(1)}°${unit === 'celsius' ? 'C' : 'F'}`;
                }
            },
            grid: {
                top: 30,
                right: 30,
                bottom: 30,
                left: 60,
                containLabel: true
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                data: hours,
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: darkMode ? '#8899aa' : '#aaaaaa',
                        width: 1
                    }
                },
                axisLabel: {
                    color: darkMode ? '#cccccc' : '#666666',
                    fontSize: 12
                }
            },
            yAxis: {
                type: 'value',
                axisLine: {
                    show: true,
                    lineStyle: {
                        color: darkMode ? '#8899aa' : '#aaaaaa',
                        width: 1
                    }
                },
                axisLabel: {
                    formatter: `{value}°${unit === 'celsius' ? 'C' : 'F'}`,
                    color: darkMode ? '#cccccc' : '#666666',
                    fontSize: 12
                },
                splitLine: {
                    show: true,
                    lineStyle: {
                        color: darkMode ? '#334455' : '#eeeeee',
                        type: 'dashed'
                    }
                }
            },
            series: [
                {
                    name: 'Temperature',
                    data: temperatures,
                    type: 'line',
                    smooth: true,
                    lineStyle: {
                        width: 3,
                        color: '#3b82f6',
                        shadowColor: 'rgba(59, 130, 246, 0.3)',
                        shadowBlur: 10
                    },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            {
                                offset: 0,
                                color: 'rgba(59, 130, 246, 0.4)'
                            },
                            {
                                offset: 1,
                                color: 'rgba(59, 130, 246, 0.05)'
                            }
                        ]),
                        shadowColor: 'rgba(59, 130, 246, 0.1)',
                        shadowBlur: 20
                    },
                    symbol: 'circle',
                    symbolSize: 8,
                    itemStyle: {
                        color: '#3b82f6',
                        borderWidth: 2,
                        borderColor: '#ffffff',
                        shadowColor: 'rgba(59, 130, 246, 0.5)',
                        shadowBlur: 5
                    }
                }
            ]
        });

        // Handle window resize
        const handleResize = () => {
            myChart.resize();
        };
        window.addEventListener('resize', handleResize);

        // Cleanup
        return () => {
            window.removeEventListener('resize', handleResize);
            myChart.dispose();
        };
    }, [unit, darkMode, hourlyData]);
    // Get Weather Data
    const fetchWeatherData = async (location: string) => {
        try {
            setWeatherError(null);
            const response = await fetch(`${API_BASE_URL}/api/location/weather?user_input=${encodeURIComponent(location)}`);
            console.log('Weather API response:', response);
            
            if (!response.ok) {
                throw new Error('Failed to fetch weather data');
            }
            
            const data: WeatherData = await response.json();
            console.log('Weather data:', data);
            setWeatherData(data);
        } catch (error) {
            console.error('Error fetching weather:', error);
            setWeatherError('Failed to fetch weather data');
            setWeatherData(null);
            throw error;  // Propagate error to caller
        }
    };
    // Get Forecast Data
    const fetchForecastData = async (location: string) => {
        try {
            setForecastError(null);
            console.log('Fetching forecast for location:', location);
            const response = await fetch(`${API_BASE_URL}/api/weather/forecast?city=${encodeURIComponent(location)}`);
            console.log('Forecast API response:', response);
            
            if (!response.ok) {
                throw new Error('Failed to fetch forecast data');
            }
            
            const data: ForecastData = await response.json();
            console.log('Parsed forecast data:', data);
            console.log('Forecast items:', data.forecast);
            
            setForecastData(data);
        } catch (error) {
            console.error('Error fetching forecast:', error);
            setForecastError('Failed to fetch forecast data');
            setForecastData(null);
            throw error;  // Propagate error to caller
        }
    };
  
    const convertTemperature = (kelvin: number | undefined): number => {
        if (!kelvin) return 0;
        if (unit === 'celsius') {
            return Math.round(kelvin - 273.15);
        }
        return Math.round((kelvin - 273.15) * 9/5 + 32);
    };

    const shareOnTwitter = () => {
        if (!weatherData) return;
        
        const tweetText = encodeURIComponent(
            `Check out the weather in ${weatherData.name}: ` +
            `${convertTemperature(weatherData.main.temp)}° ${unit === 'celsius' ? 'C' : 'F'}, ` +
            `${weatherData.weather[0].main}`
        );
        const shareUrl = encodeURIComponent(`https://weather.app/share/${weatherData.name}`);
        window.open(`https://twitter.com/intent/tweet?text=${tweetText}&url=${shareUrl}`, '_blank');
    };
   
    const shareOnFacebook = () => {
        if (!weatherData?.name) return;
        const shareUrl = encodeURIComponent(`https://weather.app/share/${weatherData.name}`);
        window.open(`https://www.facebook.com/sharer/sharer.php?u=${shareUrl}`, '_blank');
    };

    // Weather History search function
    const searchWeatherHistory = async () => {
        if (!historySearch.location || !historySearch.startDate || !historySearch.endDate) {
            setHistoryError('Please fill in all search fields.');
            return;
        }

        try {
            setIsHistoryLoading(true);
            setHistoryError(null);

            // Changed to GET method and using query parameters
            const response = await fetch(`${API_BASE_URL}/api/weather-history/location/${historySearch.location}?start_date=${encodeURIComponent(historySearch.startDate)}&end_date=${encodeURIComponent(historySearch.endDate)}`);

            if (!response.ok) {
                throw new Error('Failed to fetch weather history.');
            }

            const data = await response.json();
            setHistoryRecords(data);
        } catch (error) {
            console.error('Error fetching weather history:', error);
            setHistoryError(error instanceof Error ? error.message : 'Failed to fetch weather history.');
        } finally {
            setIsHistoryLoading(false);
        }
    };

    return (
        <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-800'}`}>
            {/* Remove full-page loading spinner */}
            <div className="max-w-7xl mx-auto px-4 pt-12 pb-6">
                {/* Header Section */}
                <header className="mb-8">
                    <div className="flex flex-col md:flex-row items-center justify-between gap-4">
                        <h1 className="text-3xl font-bold mb-4 md:mb-0">
                            <i className="fas fa-cloud-sun mr-2 text-blue-500"></i>
                            Weather Dashboard
                        </h1>
                        <div className="flex items-center gap-4 w-full md:w-auto">
                            {/* Search Bar with Search Button */}
                            <div className="relative flex w-full md:w-auto gap-2">
                                <div className="relative flex-1 min-w-[350px]">
                                    <input
                                        type="text"
                                        placeholder="Enter location: city, zip code, landmark..."
                                        value={location}
                                        onChange={(e) => setLocation(e.target.value)}
                                        onKeyPress={(e) => {
                                            if (e.key === 'Enter') {
                                                handleSelectLocation(location);
                                            }
                                        }}
                                        className={`w-full pl-10 pr-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                                            darkMode ? 'bg-gray-800 text-white border-gray-700' : 'bg-white text-gray-800 border-gray-300'
                                        } border`}
                                    />
                                    <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                                        <i className="fas fa-search"></i>
                                    </span>
                                </div>
                                
                                {/* Search Button */}
                                <button
                                    onClick={() => handleSelectLocation(location)}
                                    className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200 flex items-center gap-2 whitespace-nowrap"
                                >
                                    <i className="fas fa-search"></i>
                                    Search
                                </button>

                                {/* My Location Button */}
                                <button
                                    onClick={handleUseMyLocation}
                                    className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors duration-200 flex items-center gap-2 whitespace-nowrap"
                                >
                                    <i className="fas fa-location-arrow"></i>
                                    Current Location
                                </button>
                            </div>
                        </div>
                        {/* Unit and Theme Toggles */}
                        <div className="flex items-center gap-8">
                            <div className="flex items-center w-24 flex-shrink-0">
                                <button
                                    onClick={toggleUnit}
                                    className={`relative inline-flex h-8 w-14 items-center rounded-full cursor-pointer whitespace-nowrap !rounded-button ${unit === 'celsius' ? 'bg-blue-500' : 'bg-gray-400'}`}
                                >
                                    <span className={`inline-block h-6 w-6 transform rounded-full bg-white transition ${unit === 'celsius' ? 'translate-x-7' : 'translate-x-1'}`} />
                                </button>
                                <span className="ml-3 text-lg">°{unit === 'celsius' ? 'C' : 'F'}</span>
                            </div>
                            <button
                                onClick={toggleTheme}
                                className={`p-3 rounded-full cursor-pointer whitespace-nowrap !rounded-button ${darkMode ? 'bg-gray-700 text-yellow-400 hover:bg-gray-600' : 'bg-gray-200 text-blue-900 hover:bg-gray-300'}`}
                            >
                                <i className={`fas ${darkMode ? 'fa-sun text-xl' : 'fa-moon text-xl'}`}></i>
                            </button>
                        </div>
                    </div>
                    {error && (
                        <div className="mt-4 p-3 bg-red-100 text-red-800 rounded-lg">
                            <i className="fas fa-exclamation-circle mr-2"></i>
                            {error}
                        </div>
                    )}
                </header>
                {/* Main Content */}
                <main className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-12">
                    {/* Current Weather Section */}
                    <div className={`lg:col-span-2 rounded-xl shadow-lg overflow-hidden ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
                        <div className="p-6">
                            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
                                <div>
                                    <h2 className="text-2xl font-semibold">{weatherData?.name || 'Choose a location'}</h2>
                                    <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                                        Last updated: {new Date().toLocaleString()}
                                    </p>
                                </div>
                                <button
                                    onClick={toggleFavorite}
                                    className={`mt-2 md:mt-0 flex items-center text-sm transition-all duration-300 ${
                                        isAddingFavorite 
                                        ? 'text-orange-600 scale-110 font-bold' 
                                        : weatherData?.name && favorites.includes(weatherData.name)
                                        ? 'text-red-600 hover:text-red-700'
                                        : 'text-blue-500 hover:text-blue-600'
                                    }`}
                                >
                                    <i className={`mr-1 ${
                                        isAddingFavorite 
                                        ? 'fas fa-heart animate-pulse text-orange-600' 
                                        : weatherData?.name && favorites.includes(weatherData.name)
                                        ? 'fas fa-heart text-red-600'
                                        : 'far fa-heart text-blue-500'
                                    }`} style={{
                                        animationDuration: '0.7s'
                                    }}></i>
                                    {isAddingFavorite 
                                        ? 'Processing...' 
                                        : weatherData?.name && favorites.includes(weatherData.name)
                                        ? 'Your favorite'
                                        : 'Add to favorites'
                                    }
                                </button>
                            </div>
                            {weatherError ? (
                                <div className="text-red-500 text-center p-4">
                                    <i className="fas fa-exclamation-circle mr-2"></i>
                                    {weatherError}
                                </div>
                            ) : weatherData ? (
                                <>
                                    <div className="flex flex-col md:flex-row items-center justify-between">
                                        <div className="flex items-center mb-4 md:mb-0">
                                            <div className="text-7xl font-bold">
                                                {convertTemperature(weatherData.main.temp)}°
                                                <span className="text-3xl">{unit === 'celsius' ? 'C' : 'F'}</span>
                                            </div>
                                            <div className="ml-4 text-5xl">
                                                <i className={`fas ${
                                                    weatherData.weather[0].main === 'Clear' ? 'fa-sun text-yellow-400' :
                                                    weatherData.weather[0].main === 'Clouds' ? 'fa-cloud text-gray-400' :
                                                    weatherData.weather[0].main === 'Rain' ? 'fa-cloud-rain text-blue-400' :
                                                    'fa-cloud-sun text-yellow-400'
                                                }`}></i>
                                            </div>
                                        </div>
                                        <div className="space-y-2">
                                            <div className="text-xl">{weatherData.weather[0].main}</div>
                                            <div className={`text-sm ${darkMode ? 'text-blue-300' : 'text-blue-600'}`}>
                                                <i className="fas fa-info-circle mr-2"></i>
                                                {weatherData.weather[0].description}
                                            </div>
                                        </div>
                                    </div>
                                    {/* Weather Details Grid */}
                                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
                                        <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                                            <div className="flex items-center">
                                                <i className="fas fa-tint text-blue-500 mr-2"></i>
                                                <span className={darkMode ? 'text-gray-300' : 'text-gray-600'}>Humidity</span>
                                            </div>
                                            <div className="text-xl font-semibold mt-1">{weatherData.main.humidity}%</div>
                                        </div>
                                        <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                                            <div className="flex items-center">
                                                <i className="fas fa-wind text-blue-500 mr-2"></i>
                                                <span className={darkMode ? 'text-gray-300' : 'text-gray-600'}>Wind</span>
                                            </div>
                                            <div className="text-xl font-semibold mt-1">{weatherData.wind.speed} m/s</div>
                                        </div>
                                        <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                                            <div className="flex items-center">
                                                <i className="fas fa-sun text-yellow-500 mr-2"></i>
                                                <span className={darkMode ? 'text-gray-300' : 'text-gray-600'}>Sunrise</span>
                                            </div>
                                            <div className="text-xl font-semibold mt-1">
                                                {weatherData.sys?.sunrise ? new Date(weatherData.sys.sunrise * 1000).toLocaleTimeString() : '--:--'}
                                            </div>
                                        </div>
                                        <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                                            <div className="flex items-center">
                                                <i className="fas fa-moon text-indigo-400 mr-2"></i>
                                                <span className={darkMode ? 'text-gray-300' : 'text-gray-600'}>Sunset</span>
                                            </div>
                                            <div className="text-xl font-semibold mt-1">
                                                {weatherData.sys?.sunset ? new Date(weatherData.sys.sunset * 1000).toLocaleTimeString() : '--:--'}
                                            </div>
                                        </div>
                                    </div>
                                </>
                            ) : (
                                <div className="text-center p-4 text-gray-500">
                                    <i className="fas fa-search mr-2"></i>
                                    Search or select a location
                                </div>
                            )}
                            {/* Temperature Chart */}
                            <div className="mt-8">
                                <h3 className="text-lg font-semibold mb-4">Hourly Forecast</h3>
                                <div id="temperature-chart" className="w-full h-64"></div>
                            </div>
                        </div>
                    </div>
                    {/* Map and Favorites Section */}
                    <div className="space-y-6">
                        {/* Google Map */}
                        <div className={`rounded-xl shadow-lg overflow-hidden ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
                            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                                <h3 className="font-semibold">Location Map</h3>
                            </div>
                            <div className="h-64 bg-gray-300 dark:bg-gray-700 relative overflow-hidden">
                                {mapError ? (
                                    <div className="absolute inset-0 flex items-center justify-center text-red-500">
                                        <i className="fas fa-exclamation-circle mr-2"></i>
                                        {mapError}
                                    </div>
                                ) : mapUrl ? (
                                    <iframe
                                        src={mapUrl}
                                        className="w-full h-full border-0"
                                        allowFullScreen
                                        loading="lazy"
                                        referrerPolicy="no-referrer-when-downgrade"
                                    ></iframe>
                                ) : (
                                    <div className="absolute inset-0 flex items-center justify-center">
                                        <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500"></div>
                                    </div>
                                )}
                            </div>
                        </div>
                        {/* Favorites Section */}
                        <div className={`rounded-xl shadow-lg overflow-hidden ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
                            <div
                                className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between cursor-pointer"
                                onClick={toggleFavorites}
                            >
                                <h3 className="font-semibold">Favorite Locations</h3>
                                <i className={`fas ${showFavorites ? 'fa-chevron-up' : 'fa-chevron-down'} text-gray-500`}></i>
                            </div>
                            {showFavorites && (
                                <div className="p-4">
                                    {favorites.length > 0 ? (
                                        <ul className="space-y-2">
                                            {favorites.map((fav, index) => (
                                                <li key={index} className="flex items-center justify-between">
                                                    <button
                                                        className="text-left hover:text-blue-500 cursor-pointer whitespace-nowrap !rounded-button"
                                                        onClick={() => handleSelectLocation(fav)}
                                                    >
                                                        {fav}
                                                    </button>
                                                    <button
                                                        className="text-red-500 hover:text-red-600 cursor-pointer whitespace-nowrap !rounded-button"
                                                        onClick={() => removeFavorite(fav)}
                                                    >
                                                        <i className="fas fa-times"></i>
                                                    </button>
                                                </li>
                                            ))}
                                        </ul>
                                    ) : (
                                        <p className="text-gray-500 dark:text-gray-400 text-sm">No favorite locations saved yet.</p>
                                    )}
                                </div>
                            )}
                        </div>
                        {/* Data Export and Sharing Section */}
                        <div className={`rounded-xl shadow-lg overflow-hidden ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
                            <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                                <h3 className="font-semibold">Export & Share</h3>
                            </div>
                            <div className="p-4 flex flex-wrap items-center gap-6">
                                <div className="flex items-center gap-4">
                                    <button
                                        onClick={() => exportData('csv')}
                                        className="flex items-center justify-center w-10 h-10 bg-emerald-400 text-white rounded-lg hover:bg-emerald-500 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
                                        title="Export as CSV"
                                    >
                                        <i className="fas fa-file-csv text-lg"></i>
                                    </button>
                                    <button
                                        onClick={() => exportData('json')}
                                        className="flex items-center justify-center w-10 h-10 bg-amber-400 text-white rounded-lg hover:bg-amber-500 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
                                        title="Export as JSON"
                                    >
                                        <i className="fas fa-file-code text-lg"></i>
                                    </button>
                                    <button
                                        onClick={() => window.print()}
                                        className="flex items-center justify-center w-10 h-10 bg-gray-400 text-white rounded-lg hover:bg-gray-500 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
                                        title="Print weather report"
                                    >
                                        <i className="fas fa-print text-lg"></i>
                                    </button>
                                </div>
                                <div className="h-8 w-px bg-gray-300 dark:bg-gray-600"></div>
                                <div className="flex items-center gap-4">
                                    <button
                                        onClick={() => {
                                            if (!weatherData?.name) return;
                                            const url = `https://weather.app/share/${weatherData.name}`;
                                            navigator.clipboard.writeText(url);
                                            alert('Link copied to clipboard!');
                                        }}
                                        className="flex items-center justify-center w-10 h-10 bg-blue-400 text-white rounded-lg hover:bg-blue-500 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
                                        title="Copy share link"
                                    >
                                        <i className="fas fa-link text-lg"></i>
                                    </button>
                                    <button
                                        onClick={shareOnTwitter}
                                        disabled={!weatherData}
                                        className={`flex items-center justify-center w-10 h-10 rounded-lg transition-colors duration-200 ${
                                            weatherData 
                                            ? 'bg-sky-400 text-white hover:bg-sky-500' 
                                            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                        }`}
                                        title="Share on Twitter"
                                    >
                                        <i className="fab fa-twitter text-lg"></i>
                                    </button>
                                    <button
                                        onClick={shareOnFacebook}
                                        disabled={!weatherData}
                                        className={`flex items-center justify-center w-10 h-10 rounded-lg transition-colors duration-200 ${
                                            weatherData 
                                            ? 'bg-indigo-400 text-white hover:bg-indigo-500' 
                                            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                                        }`}
                                        title="Share on Facebook"
                                    >
                                        <i className="fab fa-facebook-f text-lg"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>

                    
                </main>

                {/* 5-Day Forecast */}
                <section className="mt-16">
                    <h2 className="text-2xl font-semibold mb-6">5-Day Forecast</h2>
                    {loading ? (
                        <div className="text-center p-4 rounded-xl shadow-lg bg-white dark:bg-gray-800">
                            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500 mx-auto"></div>
                            <p className="mt-2 text-gray-500">Loading weather forecast...</p>
                        </div>
                    ) : forecastError ? (
                        <div className="text-red-500 text-center p-4 rounded-xl shadow-lg bg-white dark:bg-gray-800">
                            <i className="fas fa-exclamation-circle mr-2"></i>
                            {forecastError}
                        </div>
                    ) : !forecastData || !forecastData.forecast ? (
                        <div className="text-center p-4 rounded-xl shadow-lg bg-white dark:bg-gray-800">
                            <i className="fas fa-cloud text-4xl mb-2 text-gray-400"></i>
                            <p className="text-gray-500">Choose a location to load weather forecast</p>
                        </div>
                    ) : (() => {
                        // Group data by date
                        const dailyForecasts = forecastData.forecast.reduce((acc, item) => {
                            const date = item.forecast_date;
                            if (!acc[date]) {
                                acc[date] = item;
                            }
                            return acc;
                        }, {} as Record<string, ForecastItem>);

                        // Sort by date
                        const sortedForecasts = Object.values(dailyForecasts).sort((a, b) => 
                            new Date(a.forecast_date).getTime() - new Date(b.forecast_date).getTime()
                        ).slice(0, 5);

                        console.log('Processed daily forecasts:', sortedForecasts);

                        return (
                            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
                                {sortedForecasts.map((item, index) => (
                                    <div
                                        key={index}
                                        className={`p-4 rounded-xl shadow-lg ${darkMode ? 'bg-gray-800' : 'bg-white'}`}
                                    >
                                        <div className="text-center">
                                            <h3 className="font-bold text-lg">
                                                {new Date(item.forecast_date).toLocaleDateString([], { weekday: 'short' })}
                                            </h3>
                                            <div className="my-4 text-4xl">
                                                <i className={`fas ${
                                                    item.condition === 'Clear' ? 'fa-sun text-yellow-400' :
                                                    item.condition === 'Clouds' ? 'fa-cloud text-gray-400' :
                                                    item.condition === 'Rain' ? 'fa-cloud-rain text-blue-400' :
                                                    'fa-cloud-sun text-yellow-400'
                                                }`}></i>
                                            </div>
                                            <p className="text-sm mb-2">{item.condition}</p>
                                            <div className="flex justify-between items-center">
                                                <span className="font-semibold text-lg text-red-500">
                                                    {unit === 'celsius' ? Math.round(item.temp_c) : Math.round(item.temp_f)}°
                                                </span>
                                                <span className="font-semibold text-lg text-blue-500">
                                                    {unit === 'celsius' ? Math.round(item.temp_c - 5) : Math.round(item.temp_f - 9)}°
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        );
                    })()}
                </section>

                {/* Weather History Search Section */}
                <section className={`weather-history-section mt-16 p-6 rounded-xl shadow-lg ${darkMode ? "bg-gray-800" : "bg-white"}`}>
                    <h2 className="history-section-title text-2xl font-semibold mb-6">
                        <i className="fas fa-history mr-2"></i>
                        Weather History Lookup
                    </h2>
                    <div className="history-search-controls flex flex-wrap gap-4">
                        <div className="history-location-input flex-1 min-w-[200px]">
                            <div className="input-wrapper relative">
                                <input
                                    type="text"
                                    placeholder="Enter location"
                                    value={historySearch.location}
                                    onChange={(e) => setHistorySearch({
                                        ...historySearch,
                                        location: e.target.value
                                    })}
                                    className={`w-full pl-10 pr-4 py-2 rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                                        darkMode
                                        ? "bg-gray-700 border-gray-600 text-white"
                                        : "bg-white border-gray-300"
                                    }`}
                                />
                                <i className="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                            </div>
                        </div>
                        <div className="flex-1 min-w-[200px]">
                            <div className="relative">
                                <input
                                    type="date"
                                    value={historySearch.startDate}
                                    onChange={(e) => setHistorySearch({
                                        ...historySearch,
                                        startDate: e.target.value
                                    })}
                                    className={`w-full pl-10 pr-4 py-2 rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                                        darkMode
                                        ? "bg-gray-700 border-gray-600 text-white"
                                        : "bg-white border-gray-300"
                                    }`}
                                />
                                <i className="fas fa-calendar absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                            </div>
                        </div>
                        <div className="flex-1 min-w-[200px]">
                            <div className="relative">
                                <input
                                    type="date"
                                    value={historySearch.endDate}
                                    onChange={(e) => setHistorySearch({
                                        ...historySearch,
                                        endDate: e.target.value
                                    })}
                                    className={`w-full pl-10 pr-4 py-2 rounded-lg border focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                                        darkMode
                                        ? "bg-gray-700 border-gray-600 text-white"
                                        : "bg-white border-gray-300"
                                    }`}
                                />
                                <i className="fas fa-calendar absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400"></i>
                            </div>
                        </div>
                        <button 
                            onClick={searchWeatherHistory}
                            disabled={isHistoryLoading}
                            className={`px-6 py-2 text-white rounded-lg transition-colors duration-200 flex items-center whitespace-nowrap !rounded-button ${
                                isHistoryLoading 
                                ? 'bg-gray-500 cursor-not-allowed' 
                                : 'bg-blue-500 hover:bg-blue-600'
                            }`}
                        >
                            {isHistoryLoading ? (
                                <>
                                    <i className="fas fa-spinner fa-spin mr-2"></i>
                                    Searching...
                                </>
                            ) : (
                                <>
                                    <i className="fas fa-search mr-2"></i>
                                    Search Records
                                </>
                            )}
                        </button>
                    </div>

                    {/* Error Message */}
                    {historyError && (
                        <div className="mt-4 p-3 bg-red-100 text-red-800 rounded-lg">
                            <i className="fas fa-exclamation-circle mr-2"></i>
                            {historyError}
                        </div>
                    )}

                    {/* Results Table */}
                    {historyRecords.length > 0 && (
                        <div className="mt-6 overflow-x-auto">
                            <table className={`min-w-full divide-y divide-gray-200 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                                <thead>
                                    <tr>
                                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Date</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Temperature</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Weather</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Humidity</th>
                                        <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider">Wind Speed</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200">
                                    {historyRecords.map((record) => (
                                        <tr key={record.id} className={darkMode ? 'bg-gray-700' : 'bg-white'}>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                {new Date(record.date).toLocaleDateString()}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">
                                                {unit === 'celsius' ? record.temperature : (record.temperature * 9/5) + 32}°{unit === 'celsius' ? 'C' : 'F'}
                                            </td>
                                            <td className="px-6 py-4 whitespace-nowrap">{record.condition}</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{record.humidity}%</td>
                                            <td className="px-6 py-4 whitespace-nowrap">{record.wind_speed} m/s</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </section>
                {/* Weather Videos and Share Section */}
                <section className="mt-16">
                    <h2 className="text-2xl font-semibold mb-6">Travel Guide & Local Insights</h2>
                    {videoError ? (
                        <div className="text-red-500 text-center p-4 rounded-xl shadow-lg bg-white dark:bg-gray-800">
                            <i className="fas fa-exclamation-circle mr-2"></i>
                            {videoError}
                        </div>
                    ) : videos.length > 0 ? (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {/* Weather Video */}
                            {videos.filter(video => video.category === 'weather').map((video) => (
                                <div key={video.videoId} className={`rounded-xl shadow-lg overflow-hidden ${
                                    darkMode ? 'bg-gray-800' : 'bg-white'
                                }`}>
                                    <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                                        <h3 className="font-semibold flex items-center">
                                            <i className="fas fa-cloud-sun text-blue-500 mr-2"></i>
                                            Weather Forecast
                                        </h3>
                                    </div>
                                    <div className="aspect-video">
                                        <iframe
                                            className="w-full h-full"
                                            src={video.embed_url}
                                            title={video.title}
                                            frameBorder="0"
                                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                            allowFullScreen>
                                        </iframe>
                                    </div>
                                </div>
                            ))}
                            
                            {/* Restaurant Video */}
                            {videos.filter(video => video.category === 'restaurants').map((video) => (
                                <div key={video.videoId} className={`rounded-xl shadow-lg overflow-hidden ${
                                    darkMode ? 'bg-gray-800' : 'bg-white'
                                }`}>
                                    <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                                        <h3 className="font-semibold flex items-center">
                                            <i className="fas fa-utensils text-red-500 mr-2"></i>
                                            Best Restaurants
                                        </h3>
                                    </div>
                                    <div className="aspect-video">
                                        <iframe
                                            className="w-full h-full"
                                            src={video.embed_url}
                                            title={video.title}
                                            frameBorder="0"
                                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                            allowFullScreen>
                                        </iframe>
                                    </div>
                                </div>
                            ))}
                            
                            {/* Weekend Events Video */}
                            {videos.filter(video => video.category === 'weekend').map((video) => (
                                <div key={video.videoId} className={`rounded-xl shadow-lg overflow-hidden ${
                                    darkMode ? 'bg-gray-800' : 'bg-white'
                                }`}>
                                    <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                                        <h3 className="font-semibold flex items-center">
                                            <i className="fas fa-calendar-week text-green-500 mr-2"></i>
                                            Weekend Events
                                        </h3>
                                    </div>
                                    <div className="aspect-video">
                                        <iframe
                                            className="w-full h-full"
                                            src={video.embed_url}
                                            title={video.title}
                                            frameBorder="0"
                                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                            allowFullScreen>
                                        </iframe>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-8 rounded-xl shadow-lg bg-white dark:bg-gray-800">
                            <i className="fas fa-spinner fa-spin text-4xl mb-4"></i>
                            <p>Loading travel guides and local insights...</p>
                        </div>
                    )}
                </section>
            </div>
            {/* Print-only Weather Summary */}
            <div className="hidden print:block p-8">
                <h1 className="text-3xl font-bold mb-6">Weather Report - {weatherData?.name || 'Choose a location'}</h1>
                <div className="mb-6">
                    <p className="text-lg">Generated on: {new Date().toLocaleString()}</p>
                    <p className="text-lg">Current Temperature: {convertTemperature(weatherData?.main.temp || 0)}°{unit === 'celsius' ? 'C' : 'F'}</p>
                    <p className="text-lg">Condition: {weatherData?.weather[0].main || 'Choose a location'}</p>
                </div>
                <div className="grid grid-cols-2 gap-4 mb-6">
                    <div>
                        <h2 className="text-xl font-semibold mb-2">Current Conditions</h2>
                        <p>Humidity: {weatherData?.main?.humidity ?? 'N/A'}%</p>
                        <p>Wind Speed: {weatherData?.wind?.speed ?? 'N/A'} m/s</p>
                        <p>Sunrise: {weatherData?.sys?.sunrise ? new Date(weatherData.sys.sunrise * 1000).toLocaleTimeString() : 'N/A'}</p>
                        <p>Sunset: {weatherData?.sys?.sunset ? new Date(weatherData.sys.sunset * 1000).toLocaleTimeString() : 'N/A'}</p>
                    </div>
                    <div>
                        <h2 className="text-xl font-semibold mb-2">5-Day Forecast</h2>
                        {forecastData?.forecast.slice(0, 5).map((item, index) => (
                            <p key={index}>
                                {new Date(item.forecast_date).toLocaleDateString([], { weekday: 'short' })}: 
                                {convertTemperature(item.temp_c)}° / {convertTemperature(item.temp_c - 5)}° - 
                                {item.condition}
                            </p>
                        ))}
                    </div>
                </div>
                <div className="text-sm text-gray-500">
                    <p>Weather Dashboard - https://weather.app</p>
                    <p>Report generated for: {weatherData?.name || 'Choose a location'}</p>
                </div>
            </div>
            
            {/* Footer */}
            <footer className={`mt-20 py-12 ${darkMode ? 'bg-gray-800 text-gray-300' : 'bg-gray-100 text-gray-600'}`}>
                <div className="max-w-7xl mx-auto px-4">
                    <div className="text-center space-y-2">
                        <p className="text-lg font-medium">Weather Dashboard &copy; 2025. All rights reserved.</p>
                        <p className="text-sm">Last updated: May 27, 2025</p>
                        <p className={`text-sm ${darkMode ? 'text-blue-300' : 'text-blue-600'}`}>
                            Developer: Nabin Kim | PM Accelerator 2025
                        </p>
                        <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                            PM Accelerator: Innovative Product Manager Training Program
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    );
}

export default App;