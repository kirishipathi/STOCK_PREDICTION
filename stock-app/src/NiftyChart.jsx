import React, { useEffect, useState } from "react";

import { Line } from "react-chartjs-2";

import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
  Filler
);

function NiftyChart() {

  const [chartData, setChartData] = useState(null);

  const [marketData, setMarketData] = useState(null);

  const [lastUpdated, setLastUpdated] = useState("");

  useEffect(() => {

    const fetchData = () => {

      fetch("http://127.0.0.1:8000/nifty_live")

        .then((res) => res.json())

        .then((data) => {

          setMarketData(data);

          setLastUpdated(
            new Date().toLocaleTimeString()
          );

          setChartData({

            labels: data.chart_data.map(
              (item) => item.time
            ),

            datasets: [

              {

                label: "NIFTY 50",

                data: data.chart_data.map(
                  (item) => item.price
                ),

                borderColor: "#00E396",

                backgroundColor:
                  "rgba(0,227,150,0.12)",

                fill: true,

                borderWidth: 3,

                pointRadius: 0,

                pointHoverRadius: 7,

                tension: 0.45
              }
            ]
          });

        })

        .catch((err) => {

          console.error(err);
        });
    };

    fetchData();

    const interval = setInterval(
      fetchData,
      30000
    );

    return () => clearInterval(interval);

  }, []);

  if (!chartData || !marketData) {

    return (

      <div
        style={{
          background: "#1e293b",
          padding: "30px",
          borderRadius: "15px",
          color: "white",
          textAlign: "center",
          fontSize: "18px"
        }}
      >
        Loading Live Market Data...
      </div>

    );
  }

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

        borderColor: "#00E396",

        borderWidth: 1,

        titleColor: "#00E396",

        bodyColor: "#ffffff",

        padding: 12,

        displayColors: false,

        callbacks: {

          title: function(context) {

            return `Time : ${context[0].label}`;
          },

          label: function(context) {

            return `Price : ₹${context.raw.toLocaleString()}`;
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

          color:
            "rgba(255,255,255,0.05)"
        }
      },

      y: {

        position: "right",

        ticks: {

          color: "#ffffff",

          callback: function(value) {

            return "₹" +
              value.toLocaleString();
          }
        },

        grid: {

          color:
            "rgba(255,255,255,0.05)"
        }
      }
    }
  };

  const cardStyle = {

    background: "#0f172a",

    padding: "15px",

    borderRadius: "12px",

    minWidth: "160px",

    textAlign: "center",

    boxShadow:
      "0 0 10px rgba(255,255,255,0.03)"
  };

  return (

    <div
      style={{
        background: "#1e293b",

        padding: "25px",

        borderRadius: "15px",

        color: "white",

        boxShadow:
          "0 0 20px rgba(0,227,150,0.15)"
      }}
    >

      <h2
        style={{
          color: "#00E396",

          textAlign: "center",

          marginBottom: "5px"
        }}
      >
        NIFTY 50 LIVE MARKET
      </h2>

      <p
        style={{
          textAlign: "center",

          color: "#22c55e",

          marginBottom: "25px",

          fontWeight: "600"
        }}
      >
        LIVE MARKET DATA
      </p>

      <div
        style={{
          display: "flex",

          justifyContent: "space-between",

          flexWrap: "wrap",

          gap: "15px",

          marginBottom: "25px"
        }}
      >

        <div style={cardStyle}>
          <h4>Current</h4>
          <p>
            ₹{marketData.current.toLocaleString()}
          </p>
        </div>

        <div style={cardStyle}>
          <h4>High</h4>
          <p>
            ₹{marketData.high.toLocaleString()}
          </p>
        </div>

        <div style={cardStyle}>
          <h4>Low</h4>
          <p>
            ₹{marketData.low.toLocaleString()}
          </p>
        </div>

        <div style={cardStyle}>
          <h4>Change</h4>

          <p
            style={{
              color:
                marketData.change >= 0
                  ? "#22c55e"
                  : "#ef4444"
            }}
          >
            {marketData.change}%
          </p>
        </div>

      </div>

      <div
        style={{
          height: "500px"
        }}
      >

        <Line
          data={chartData}
          options={options}
        />

      </div>

      <div
        style={{
          display: "flex",

          justifyContent: "space-between",

          marginTop: "20px",

          color: "#94a3b8",

          fontSize: "12px"
        }}
      >

        <span>
          Auto Refresh : 30 Seconds
        </span>

        <span>
          Last Updated : {lastUpdated}
        </span>

      </div>

    </div>
  );
}

export default NiftyChart;