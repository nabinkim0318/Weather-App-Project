// The exported code uses Tailwind CSS. Install Tailwind CSS in your dev environment to ensure all styles work.

import React, { useState, useEffect } from 'react';
import * as echarts from 'echarts';

const App: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [location, setLocation] = useState<string>('');
  const [searchResults, setSearchResults] = useState<string[]>([]);
  const [showSearchResults, setShowSearchResults] = useState<boolean>(false);
  const [unit, setUnit] = useState<'celsius' | 'fahrenheit'>('celsius');
  const [darkMode, setDarkMode] = useState<boolean>(false);
  const [showFavorites, setShowFavorites] = useState<boolean>(false);
  const [favorites, setFavorites] = useState<string[]>(['London', 'New York', 'Tokyo']);
  const [error, setError] = useState<string | null>(null);

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

  const forecastData = [
    { day: 'Wed', high: unit === 'celsius' ? 19 : 66, low: unit === 'celsius' ? 13 : 55, condition: 'Sunny' },
    { day: 'Thu', high: unit === 'celsius' ? 20 : 68, low: unit === 'celsius' ? 14 : 57, condition: 'Partly Cloudy' },
    { day: 'Fri', high: unit === 'celsius' ? 18 : 64, low: unit === 'celsius' ? 12 : 54, condition: 'Rainy' },
    { day: 'Sat', high: unit === 'celsius' ? 17 : 63, low: unit === 'celsius' ? 11 : 52, condition: 'Cloudy' },
    { day: 'Sun', high: unit === 'celsius' ? 21 : 70, low: unit === 'celsius' ? 15 : 59, condition: 'Sunny' }
  ];

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setLocation(value);
    
    if (value.length > 2) {
      // Mock search results
      setSearchResults(['San Francisco, CA', 'San Diego, CA', 'San Jose, CA', 'Santa Barbara, CA']);
      setShowSearchResults(true);
    } else {
      setSearchResults([]);
      setShowSearchResults(false);
    }
  };

  const handleSelectLocation = (location: string) => {
    setLocation(location);
    setShowSearchResults(false);
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  };

  const handleUseMyLocation = () => {
    setLoading(true);
    setError(null);
    
    // Simulate geolocation and API call
    setTimeout(() => {
      // Simulate successful geolocation
      setLocation('San Francisco, CA');
      setLoading(false);
    }, 1500);
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

  const addToFavorites = () => {
    if (currentWeather.location && !favorites.includes(currentWeather.location)) {
      setFavorites([...favorites, currentWeather.location]);
    }
  };

  const removeFavorite = (location: string) => {
    setFavorites(favorites.filter(fav => fav !== location));
  };

  const exportData = (format: 'csv' | 'json') => {
    const data = {
      current: currentWeather,
      forecast: forecastData
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
      // Simple CSV format
      let csv = 'Day,High,Low,Condition\n';
      forecastData.forEach(day => {
        csv += `${day.day},${day.high},${day.low},${day.condition}\n`;
      });
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `weather_forecast_${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
    }
  };

  // Initialize temperature chart
  useEffect(() => {
    const chartDom = document.getElementById('temperature-chart');
    if (chartDom) {
      const myChart = echarts.init(chartDom);
      
      const option = {
        animation: false,
        tooltip: {
          trigger: 'axis',
          formatter: function(params: any) {
            return `${params[0].name}: ${params[0].value}°${unit === 'celsius' ? 'C' : 'F'}`;
          }
        },
        xAxis: {
          type: 'category',
          data: ['6AM', '9AM', '12PM', '3PM', '6PM', '9PM', '12AM', '3AM'],
          axisLine: {
            lineStyle: {
              color: darkMode ? '#8899aa' : '#aaaaaa'
            }
          },
          axisLabel: {
            color: darkMode ? '#cccccc' : '#666666'
          }
        },
        yAxis: {
          type: 'value',
          axisLine: {
            lineStyle: {
              color: darkMode ? '#8899aa' : '#aaaaaa'
            }
          },
          axisLabel: {
            formatter: `{value}°${unit === 'celsius' ? 'C' : 'F'}`,
            color: darkMode ? '#cccccc' : '#666666'
          },
          splitLine: {
            lineStyle: {
              color: darkMode ? '#334455' : '#eeeeee'
            }
          }
        },
        series: [
          {
            data: unit === 'celsius' 
              ? [14, 16, 18, 19, 18, 16, 15, 14] 
              : [57, 61, 64, 66, 64, 61, 59, 57],
            type: 'line',
            smooth: true,
            lineStyle: {
              width: 3,
              color: '#3b82f6'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgba(59, 130, 246, 0.5)'
                },
                {
                  offset: 1,
                  color: 'rgba(59, 130, 246, 0.1)'
                }
              ])
            },
            symbol: 'circle',
            symbolSize: 8,
            itemStyle: {
              color: '#3b82f6'
            }
          }
        ]
      };

      option && myChart.setOption(option);
      
      // Cleanup
      return () => {
        myChart.dispose();
      };
    }
  }, [unit, darkMode]);

  return (
    <div className={`min-h-screen transition-colors duration-300 ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-800'}`}>
      {/* Loading Spinner */}
      {loading && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 z-50">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500"></div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 py-6">
        {/* Header Section */}
        <header className="mb-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <h1 className="text-3xl font-bold mb-4 md:mb-0">
              <i className="fas fa-cloud-sun mr-2 text-blue-500"></i>
              Weather Dashboard
            </h1>
            
            <div className="flex items-center gap-4 w-full md:w-auto">
              {/* Search Bar */}
              <div className="relative w-full md:w-80">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search location..."
                    value={location}
                    onChange={handleSearch}
                    className={`w-full pl-10 pr-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${darkMode ? 'bg-gray-800 text-white border-gray-700' : 'bg-white text-gray-800 border-gray-300'} border`}
                  />
                  <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400">
                    <i className="fas fa-search"></i>
                  </span>
                </div>
                
                {showSearchResults && searchResults.length > 0 && (
                  <div className={`absolute z-10 w-full mt-1 rounded-lg shadow-lg ${darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'} border`}>
                    <ul>
                      {searchResults.map((result, index) => (
                        <li 
                          key={index}
                          className={`px-4 py-2 cursor-pointer hover:bg-blue-100 hover:text-blue-800 ${darkMode ? 'hover:bg-gray-700 hover:text-blue-300' : ''}`}
                          onClick={() => handleSelectLocation(result)}
                        >
                          {result}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
              
              {/* Use My Location Button */}
              <button 
                onClick={handleUseMyLocation}
                className="flex items-center justify-center px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
              >
                <i className="fas fa-location-arrow mr-2"></i>
                My Location
              </button>
            </div>
            
            {/* Unit and Theme Toggles */}
            <div className="flex items-center gap-4">
              <div className="flex items-center">
                <button 
                  onClick={toggleUnit}
                  className={`relative inline-flex h-6 w-11 items-center rounded-full cursor-pointer whitespace-nowrap !rounded-button ${unit === 'celsius' ? 'bg-blue-500' : 'bg-gray-400'}`}
                >
                  <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition ${unit === 'celsius' ? 'translate-x-6' : 'translate-x-1'}`} />
                </button>
                <span className="ml-2">°{unit === 'celsius' ? 'C' : 'F'}</span>
              </div>
              
              <button 
                onClick={toggleTheme}
                className={`p-2 rounded-full cursor-pointer whitespace-nowrap !rounded-button ${darkMode ? 'bg-gray-700 text-yellow-300' : 'bg-gray-200 text-gray-700'}`}
              >
                <i className={`fas ${darkMode ? 'fa-sun' : 'fa-moon'}`}></i>
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
        <main className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Current Weather Section */}
          <div className={`lg:col-span-2 rounded-xl shadow-lg overflow-hidden ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
            <div className="p-6">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
                <div>
                  <h2 className="text-2xl font-semibold">{currentWeather.location}</h2>
                  <p className={`text-sm ${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                    Last updated: {currentWeather.lastUpdated}
                  </p>
                </div>
                
                <button 
                  onClick={addToFavorites}
                  className="mt-2 md:mt-0 flex items-center text-sm text-blue-500 hover:text-blue-600 cursor-pointer whitespace-nowrap !rounded-button"
                >
                  <i className="fas fa-heart mr-1"></i>
                  Add to favorites
                </button>
              </div>
              
              <div className="flex flex-col md:flex-row items-center justify-between">
                <div className="flex items-center mb-4 md:mb-0">
                  <div className="text-7xl font-bold">
                    {currentWeather.temperature}°
                    <span className="text-3xl">{unit === 'celsius' ? 'C' : 'F'}</span>
                  </div>
                  <div className="ml-4 text-5xl">
                    <i className={`fas fa-cloud-sun text-yellow-400`}></i>
                  </div>
                </div>
                
                <div className="text-xl">{currentWeather.condition}</div>
              </div>
              
              {/* Weather Details Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                  <div className="flex items-center">
                    <i className="fas fa-tint text-blue-500 mr-2"></i>
                    <span className={darkMode ? 'text-gray-300' : 'text-gray-600'}>Humidity</span>
                  </div>
                  <div className="text-xl font-semibold mt-1">{currentWeather.humidity}%</div>
                </div>
                
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                  <div className="flex items-center">
                    <i className="fas fa-wind text-blue-500 mr-2"></i>
                    <span className={darkMode ? 'text-gray-300' : 'text-gray-600'}>Wind</span>
                  </div>
                  <div className="text-xl font-semibold mt-1">{currentWeather.windSpeed}</div>
                </div>
                
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                  <div className="flex items-center">
                    <i className="fas fa-sun text-yellow-500 mr-2"></i>
                    <span className={darkMode ? 'text-gray-300' : 'text-gray-600'}>Sunrise</span>
                  </div>
                  <div className="text-xl font-semibold mt-1">{currentWeather.sunrise}</div>
                </div>
                
                <div className={`p-4 rounded-lg ${darkMode ? 'bg-gray-700' : 'bg-gray-100'}`}>
                  <div className="flex items-center">
                    <i className="fas fa-moon text-indigo-400 mr-2"></i>
                    <span className={darkMode ? 'text-gray-300' : 'text-gray-600'}>Sunset</span>
                  </div>
                  <div className="text-xl font-semibold mt-1">{currentWeather.sunset}</div>
                </div>
              </div>
              
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
                <img 
                  src="https://readdy.ai/api/search-image?query=A%20detailed%20satellite%20map%20view%20of%20San%20Francisco%20showing%20the%20downtown%20area%2C%20Golden%20Gate%20Bridge%2C%20and%20Bay%20Area%20with%20clear%20geographical%20features%20and%20landmarks%2C%20high%20resolution%20satellite%20imagery&width=600&height=300&seq=1&orientation=landscape" 
                  alt="Map of San Francisco"
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="bg-blue-500 h-6 w-6 rounded-full flex items-center justify-center">
                    <div className="bg-white h-2 w-2 rounded-full"></div>
                  </div>
                </div>
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
            
            {/* Export Section */}
            <div className={`rounded-xl shadow-lg overflow-hidden ${darkMode ? 'bg-gray-800' : 'bg-white'}`}>
              <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                <h3 className="font-semibold">Export Data</h3>
              </div>
              <div className="p-4 flex flex-col sm:flex-row gap-3">
                <button 
                  onClick={() => exportData('csv')}
                  className="flex-1 flex items-center justify-center px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
                >
                  <i className="fas fa-file-csv mr-2"></i>
                  Export CSV
                </button>
                <button 
                  onClick={() => exportData('json')}
                  className="flex-1 flex items-center justify-center px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors duration-200 cursor-pointer whitespace-nowrap !rounded-button"
                >
                  <i className="fas fa-file-code mr-2"></i>
                  Export JSON
                </button>
              </div>
            </div>
          </div>
        </main>
        
        {/* 5-Day Forecast */}
        <section className="mt-8">
          <h2 className="text-2xl font-semibold mb-4">5-Day Forecast</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
            {forecastData.map((day, index) => (
              <div 
                key={index}
                className={`p-4 rounded-xl shadow-lg ${darkMode ? 'bg-gray-800' : 'bg-white'}`}
              >
                <div className="text-center">
                  <h3 className="font-bold text-lg">{day.day}</h3>
                  <div className="my-4 text-4xl">
                    <i className={`fas ${
                      day.condition === 'Sunny' ? 'fa-sun text-yellow-400' :
                      day.condition === 'Partly Cloudy' ? 'fa-cloud-sun text-gray-400' :
                      day.condition === 'Cloudy' ? 'fa-cloud text-gray-400' :
                      'fa-cloud-rain text-blue-400'
                    }`}></i>
                  </div>
                  <p className="text-sm mb-2">{day.condition}</p>
                  <div className="flex justify-between items-center">
                    <span className="font-semibold">{day.high}°</span>
                    <span className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>{day.low}°</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
      </div>
      
      {/* Footer */}
      <footer className={`mt-12 py-6 ${darkMode ? 'bg-gray-800 text-gray-300' : 'bg-gray-100 text-gray-600'}`}>
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p>Weather Dashboard &copy; 2025. All rights reserved.</p>
          <p className="text-sm mt-2">Last updated: May 27, 2025</p>
        </div>
      </footer>
    </div>
  );
};

export default App;
