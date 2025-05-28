import { useEffect } from 'react';
import * as echarts from 'echarts';

interface HourlyForecastProps {
  unit: 'celsius' | 'fahrenheit';
  darkMode: boolean;
}

const HourlyForecast = ({ unit, darkMode }: HourlyForecastProps) => {
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
    <div className="mt-8">
      <h3 className="text-lg font-semibold mb-4">Hourly Forecast</h3>
      <div id="temperature-chart" className="w-full h-64"></div>
    </div>
  );
};

export default HourlyForecast;
