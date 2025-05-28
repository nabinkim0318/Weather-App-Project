interface Alert {
  type: string;
  severity: 'low' | 'medium' | 'high';
  message: string;
  time: string;
}

interface WeatherAlertsProps {
  alerts: Alert[];
  darkMode: boolean;
}

const WeatherAlerts = ({ alerts, darkMode }: WeatherAlertsProps) => {
  const getSeverityColor = (severity: Alert['severity']) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      default:
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
    }
  };

  if (!alerts || alerts.length === 0) return null;

  return (
    <div className={`rounded-xl shadow-lg overflow-hidden ${darkMode ? "bg-gray-800" : "bg-white"} mt-6`}>
      <div className="p-4 border-b border-gray-200 dark:border-gray-700">
        <h3 className="font-semibold flex items-center">
          <i className="fas fa-exclamation-triangle text-yellow-500 mr-2"></i>
          Weather Alerts
        </h3>
      </div>
      <div className="p-4">
        <div className="space-y-4">
          {alerts.map((alert, index) => (
            <div
              key={index}
              className={`p-4 rounded-lg ${getSeverityColor(alert.severity)}`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <h4 className="font-semibold">{alert.type}</h4>
                  <p className="mt-1">{alert.message}</p>
                </div>
                <span className="text-sm opacity-75">{alert.time}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default WeatherAlerts;
