import { useEffect } from 'react';
import * as echarts from 'echarts';

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

interface CurrentWeatherProps {
  currentWeather: WeatherData;
  unit: 'celsius' | 'fahrenheit';
  darkMode: boolean;
  onAddToFavorites: () => void;
}

const CurrentWeather = ({
  currentWeather,
  unit,
  darkMode,
  onAddToFavorites,
}: CurrentWeatherProps) => {
  useEffect(() => {
    const chartDom = document.getElementById("temperature-chart");
    if (!chartDom) return;

    echarts.dispose(chartDom);
    const myChart = echarts.init(chartDom);

    const option = {
      animation: false,
      backgroundColor: darkMode ? "#1f2937" : "#ffffff",
      tooltip: {
        trigger: "axis",
        formatter: function (params: any) {
          return `${params[0].name}: ${params[0].value}°${unit === "celsius" ? "C" : "F"}`;
        },
      },
      grid: {
        top: 30,
        right: 30,
        bottom: 30,
        left: 60,
        containLabel: true,
      },
      xAxis: {
        type: "category",
        boundaryGap: false,
        data: ["6AM", "9AM", "12PM", "3PM", "6PM", "9PM", "12AM", "3AM"],
        axisLine: {
          show: true,
          lineStyle: {
            color: darkMode ? "#8899aa" : "#aaaaaa",
            width: 1,
          },
        },
        axisLabel: {
          color: darkMode ? "#cccccc" : "#666666",
          fontSize: 12,
        },
      },
      yAxis: {
        type: "value",
        axisLine: {
          show: true,
          lineStyle: {
            color: darkMode ? "#8899aa" : "#aaaaaa",
            width: 1,
          },
        },
        axisLabel: {
          formatter: `{value}°${unit === "celsius" ? "C" : "F"}`,
          color: darkMode ? "#cccccc" : "#666666",
          fontSize: 12,
        },
        splitLine: {
          show: true,
          lineStyle: {
            color: darkMode ? "#334455" : "#eeeeee",
            type: "dashed",
          },
        },
      },
      series: [
        {
          name: "Temperature",
          data: unit === "celsius"
            ? [14, 16, 18, 19, 18, 16, 15, 14]
            : [57, 61, 64, 66, 64, 61, 59, 57],
          type: "line",
          smooth: true,
          lineStyle: {
            width: 3,
            color: "#3b82f6",
            shadowColor: "rgba(59, 130, 246, 0.3)",
            shadowBlur: 10,
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              {
                offset: 0,
                color: "rgba(59, 130, 246, 0.4)",
              },
              {
                offset: 1,
                color: "rgba(59, 130, 246, 0.05)",
              },
            ]),
            shadowColor: "rgba(59, 130, 246, 0.1)",
            shadowBlur: 20,
          },
          symbol: "circle",
          symbolSize: 8,
          itemStyle: {
            color: "#3b82f6",
            borderWidth: 2,
            borderColor: "#ffffff",
            shadowColor: "rgba(59, 130, 246, 0.5)",
            shadowBlur: 5,
          },
        },
      ],
    };

    myChart.setOption(option);

    const handleResize = () => {
      myChart.resize();
    };
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
      myChart.dispose();
    };
  }, [unit, darkMode]);

  return (
    <div className={`lg:col-span-2 rounded-xl shadow-lg overflow-hidden ${darkMode ? "bg-gray-800" : "bg-white"}`}>
      <div className="p-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
          <div>
            <h2 className="text-2xl font-semibold">
              {currentWeather.location}
            </h2>
            <p className={`text-sm ${darkMode ? "text-gray-400" : "text-gray-500"}`}>
              Last updated: {currentWeather.lastUpdated}
            </p>
          </div>
          <button
            onClick={onAddToFavorites}
            className="mt-2 md:mt-0 flex items-center text-sm text-blue-500 hover:text-blue-600 cursor-pointer"
          >
            <i className="fas fa-heart mr-1"></i>
            Add to favorites
          </button>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-between">
          <div className="flex items-center mb-4 md:mb-0">
            <div className="text-7xl font-bold">
              {currentWeather.temperature}°
              <span className="text-3xl">
                {unit === "celsius" ? "C" : "F"}
              </span>
            </div>
            <div className="ml-4 text-5xl">
              <i className="fas fa-cloud-sun text-yellow-400"></i>
            </div>
          </div>
          <div className="space-y-2">
            <div className="text-xl">{currentWeather.condition}</div>
            <div className={`text-sm ${darkMode ? "text-blue-300" : "text-blue-600"}`}>
              <i className="fas fa-info-circle mr-2"></i>
              {currentWeather.condition === "Partly Cloudy"
                ? "Perfect day for outdoor activities!"
                : currentWeather.condition === "Rainy"
                  ? "Don't forget your umbrella today!"
                  : currentWeather.condition === "Sunny"
                    ? "Remember to wear sunscreen!"
                    : "Stay comfortable and dress appropriately!"}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-8">
          <WeatherDetail
            icon="fa-tint"
            iconColor="text-blue-500"
            label="Humidity"
            value={`${currentWeather.humidity}%`}
            darkMode={darkMode}
          />
          <WeatherDetail
            icon="fa-wind"
            iconColor="text-blue-500"
            label="Wind"
            value={currentWeather.windSpeed}
            darkMode={darkMode}
          />
          <WeatherDetail
            icon="fa-sun"
            iconColor="text-yellow-500"
            label="Sunrise"
            value={currentWeather.sunrise}
            darkMode={darkMode}
          />
          <WeatherDetail
            icon="fa-moon"
            iconColor="text-indigo-400"
            label="Sunset"
            value={currentWeather.sunset}
            darkMode={darkMode}
          />
        </div>

        <div className="mt-8">
          <h3 className="text-lg font-semibold mb-4">Hourly Forecast</h3>
          <div id="temperature-chart" className="w-full h-64"></div>
        </div>
      </div>
    </div>
  );
};

interface WeatherDetailProps {
  icon: string;
  iconColor: string;
  label: string;
  value: string;
  darkMode: boolean;
}

const WeatherDetail = ({ icon, iconColor, label, value, darkMode }: WeatherDetailProps) => (
  <div className={`p-4 rounded-lg ${darkMode ? "bg-gray-700" : "bg-gray-100"}`}>
    <div className="flex items-center">
      <i className={`fas ${icon} ${iconColor} mr-2`}></i>
      <span className={darkMode ? "text-gray-300" : "text-gray-600"}>
        {label}
      </span>
    </div>
    <div className="text-xl font-semibold mt-1">
      {value}
    </div>
  </div>
);

export default CurrentWeather;
