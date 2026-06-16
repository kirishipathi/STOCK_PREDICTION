import {
  Line
} from "react-chartjs-2";

function ForecastChart({

  currentPrice,

  forecast

}) {

  const labels = [

    "NOW",

    ...forecast.map(
      item => item.time
    )
  ];

  const forecastPrices = [

    currentPrice,

    ...forecast.map(
      item => item.price
    )
  ];

  const data = {

    labels,

    datasets: [

      {

        label: "AI Forecast",

        data: forecastPrices,

        borderColor: "#ff00ff",

        backgroundColor:
          "rgba(255,0,255,0.12)",

        borderDash: [10, 5],

        borderWidth: 3,

        fill: true,

        pointRadius: 3,

        pointHoverRadius: 8,

        tension: 0.4
      }
    ]
  };

  const options = {

    responsive: true,

    maintainAspectRatio: false,

    interaction: {

      mode: "index",

      intersect: false
    },

    plugins: {

      legend: {

        labels: {

          color: "#ffffff",

          font: {

            size: 14
          }
        }
      },

      tooltip: {

        backgroundColor: "#111827",

        borderColor: "#ff00ff",

        borderWidth: 1,

        titleColor: "#ff00ff",

        bodyColor: "#ffffff",

        callbacks: {

          title: function(context) {

            return `Time : ${context[0].label}`;
          },

          label: function(context) {

            return `Forecast : ₹${context.raw}`;
          }
        }
      }
    },

    scales: {

      x: {

        ticks: {

          color: "#ffffff",

          autoSkip: true,

          maxTicksLimit: 10
        },

        grid: {

          color: "rgba(255,255,255,0.05)"
        }
      },

      y: {

        position: "right",

        ticks: {

          color: "#ffffff",

          callback: function(value) {

            return "₹" + value;
          }
        },

        grid: {

          color: "rgba(255,255,255,0.05)"
        }
      }
    }
  };

  return (

    <div
      style={{
        background: "#1e293b",

        padding: "25px",

        borderRadius: "15px",

        marginTop: "25px",

        boxShadow:
          "0 0 20px rgba(255,0,255,0.15)"
      }}
    >

      <h2
        style={{
          color: "#38bdf8",

          textAlign: "center",

          marginBottom: "15px"
        }}
      >
         AI Forecast Path
      </h2>

      <div
        style={{
          textAlign: "center",

          color: "#94a3b8",

          marginBottom: "20px"
        }}
      >
        Predicted Market Movement
      </div>

      <div
        style={{
          height: "420px"
        }}
      >

        <Line
          data={data}
          options={options}
        />

      </div>

    </div>
  );
}

export default ForecastChart;