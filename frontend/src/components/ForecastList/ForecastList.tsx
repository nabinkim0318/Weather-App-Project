interface ForecastDay {
  day: string;
  high: number;
  low: number;
  condition: string;
}

interface ForecastListProps {
  forecastData: ForecastDay[];
  darkMode: boolean;
}

const ForecastList = ({ forecastData, darkMode }: ForecastListProps) => {
  const getWeatherIcon = (condition: string) => {
    switch (condition) {
      case "Sunny":
        return "fa-sun text-yellow-400";
      case "Partly Cloudy":
        return "fa-cloud-sun text-gray-400";
      case "Cloudy":
        return "fa-cloud text-gray-400";
      default:
        return "fa-cloud-rain text-blue-400";
    }
  };

  return (
    <section className="mt-8">
      <h2 className="text-2xl font-semibold mb-4">5-Day Forecast</h2>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4">
        {forecastData.map((day, index) => (
          <div
            key={index}
            className={`p-4 rounded-xl shadow-lg ${
              darkMode ? "bg-gray-800" : "bg-white"
            }`}
          >
            <div className="text-center">
              <h3 className="font-bold text-lg">{day.day}</h3>
              <div className="my-4 text-4xl">
                <i className={`fas ${getWeatherIcon(day.condition)}`}></i>
              </div>
              <p className="text-sm mb-2">{day.condition}</p>
              <div className="flex justify-between items-center">
                <span className="font-semibold text-lg text-red-500">
                  {day.high}°
                </span>
                <span className="font-semibold text-lg text-blue-500">
                  {day.low}°
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ForecastList;
