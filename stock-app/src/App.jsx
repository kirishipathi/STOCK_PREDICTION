import { useState, useEffect } from "react";
import axios from "axios";
import NiftyChart from "./NiftyChart";
import ForecastChart from "./ForecastChart";
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Legend,
  Tooltip,
  TimeScale,
  ScatterController
} from "chart.js";

import { Line, Chart } from "react-chartjs-2";

import {
  CandlestickController,
  CandlestickElement
} from "chartjs-chart-financial";

import "chartjs-adapter-date-fns";

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Legend,
  Tooltip,
  TimeScale,
  ScatterController,
  CandlestickController,
  CandlestickElement
);

function App() {

  // =========================
// MARKET STATUS
// =========================
const getMarketStatus = () => {
  const now = new Date();
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const current =
    hours * 60 + minutes;
  // NSE MARKET TIME
  const open = 9 * 60 + 15;
  const close = 15 * 60 + 30;
  if (current < open) {
    return {
      status: "🟡 PRE-MARKET",
      color: "#facc15"
    };
  }

  if (
    current >= open &&
    current <= close
  ) {

    return {
      status: "🟢 MARKET OPEN",
      color: "#22c55e"
    };
  }

  return {
    status: "🔴 MARKET CLOSED",
    color: "#ef4444"
  };
};

const market = getMarketStatus();

  const [symbol, setSymbol] = useState("");

  const [chartData, setChartData] = useState(null);

  const [signal, setSignal] = useState("");

  const [prediction, setPrediction] = useState(null);

  const [intradayPrediction, setIntradayPrediction] = useState(null);

  const [metrics, setMetrics] = useState(null);

  const [sentiment, setSentiment] = useState("");

  const [news, setNews] = useState([]);

  const [recommendation, setRecommendation] = useState("");

  const [confidence, setConfidence] = useState(0);

  const [timeframe, setTimeframe] = useState("1M");

  const [selectedModel, setSelectedModel] =
useState("xgboost");

  const [tickerData, setTickerData] = useState([]);

  const [marketOverview, setMarketOverview] = useState(null);

  // =========================
  // CARD STYLE
  // =========================
  const cardStyle = {
    background: "#1e293b",
    padding: "20px",
    borderRadius: "10px",
    width: "180px",
    textAlign: "center",
    boxShadow: "0 4px 10px rgba(0,0,0,0.3)"
  };

  // =========================
  // LINE CHART OPTIONS
  // =========================
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
          color: "white"
        }
      },
      tooltip: {
        enabled: true,
        backgroundColor: "#111827",
        titleColor: "#00E396",
        bodyColor: "white",
        borderColor: "#00E396",
        borderWidth: 1
      }
    },
    scales: {
      x: {
        ticks: {
          color: "white",
          maxTicksLimit: 8,
          maxRotation: 0,
          minRotation: 0
        },
        grid: {
          color: "rgba(255,255,255,0.05)"
        }
      },
      y: {

  position: "right",

  ticks: {

    color: "white",

    callback: function(value) {
      return "₹" + value;
    }
  },

  grid: {
    color: "rgba(255,255,255,0.05)"
  }
}
    },
    elements: {
      line: {
        tension: 0.35,
        borderWidth: 3
      },
      point: {
        radius: 0,
        hoverRadius: 6
      }
    }
  };


  // =========================
  // CANDLE OPTIONS
  // =========================
  const candleOptions = {

  responsive: true,

  maintainAspectRatio: false,

  plugins: {
    legend: {
      labels: {
        color: "white"
      }
    }
  },

  scales: {

    x: {
      type: "time",

      time: {
        unit: "day"
      },

      ticks: {
        color: "white"
      },

      grid: {
        color: "rgba(255,255,255,0.1)"
      }
    },

    y: {

      position: "right",

      ticks: {
        color: "white"
      },

      grid: {
        color: "rgba(255,255,255,0.1)"
      }
    }
  }
};
  // =========================
// MINI CHART OPTIONS
// =========================
const miniChartOptions = {

  ...options,

  maintainAspectRatio: false,

  scales: {

    x: {

      ticks: {

        color: "white",

        maxTicksLimit: 6
      },

      grid: {

        color:
          "rgba(255,255,255,0.05)"
      }
    },

    y: {

      ticks: {

        color: "white"
      },

      grid: {

        color:
          "rgba(255,255,255,0.05)"
      }
    }
  }
};

  // =========================
  // FETCH DATA
  // =========================
  const fetchData = async () => {

    try {

      const tickerRes = await axios.get(
        "http://127.0.0.1:8000/ticker"
      );

      setTickerData(tickerRes.data);

      const marketRes = await axios.get(
      "http://127.0.0.1:8000/market_overview"
      );

      setMarketOverview(
        marketRes.data
      );

      const res = await axios.get(
        `http://127.0.0.1:8000/chart/${symbol}?timeframe=${timeframe}`
      );

      const sentimentRes = await axios.get(
        `http://127.0.0.1:8000/sentiment/${symbol}`
      );

      const recommendationRes = await axios.get(
        `http://127.0.0.1:8000/recommendation/${symbol}`
      );

      setRecommendation(
        recommendationRes.data.recommendation
      );

      setConfidence(
        recommendationRes.data.confidence
      );

      setSentiment(
        sentimentRes.data.overall_sentiment
      );

      const predictRes = await fetch(
        `http://127.0.0.1:8000/predict/${symbol}`
      );
      const predictData = await predictRes.json();

      setPrediction(predictData);

      const intradayRes = await fetch(
        `http://127.0.0.1:8000/intraday_predict/${selectedModel}/${symbol}`
      );
      const intradayData = await intradayRes.json();
      
      setIntradayPrediction(intradayData);

      setNews(
        sentimentRes.data.news
      );

      const stockData = res.data.chart;

      // LIMIT 1M DATA SIZE

const optimizedData =

timeframe === "1M"

? stockData.slice(-120)

: stockData;

      const metrics = res.data.metrics;

      setMetrics(metrics);

      setSignal(metrics.signal);

      const labels = optimizedData.map((item) =>
        new Date(item.Date).toLocaleDateString()
      );

      // =========================
      // NORMAL CHART DATA
      // =========================
      const prices = optimizedData.map(
        (item) => item.Close
      );

      const futurePrices =

      intradayData &&
      intradayData.session_forecast &&
      Array.isArray(
        intradayData.session_forecast
      )

      ? intradayData.session_forecast
    .slice(0, 15)
    .map(item => item.price)

      : [];

      const sma = optimizedData.map(
        (item) => item.SMA_5
      );

      const rsi = optimizedData.map(
        (item) => item.RSI
      );

      const macd = optimizedData.map(
        (item) => item.MACD
      );

      const signalLine = optimizedData.map(
        (item) => item.Signal_Line
      );

      const volume = optimizedData.map(
        (item) => item.Volume
      );

      const bbUpper = optimizedData.map(
        (item) => item.BB_Upper
      );
      
      const bbMiddle = optimizedData.map(
        (item) => item.BB_Middle
      );
      const bbLower = optimizedData.map(
        (item) => item.BB_Lower
      );

      // =========================
      // CANDLE DATA
      // =========================
      const candleData = optimizedData.map(
        (item) => ({
          x: new Date(item.Date),
          o: item.Open,
          h: item.High,
          l: item.Low,
          c: item.Close
        })
      );

      const buyMarkers = optimizedData
      .filter(item => item.Signal === "BUY")
      .map(item => ({
        x: new Date(item.Date),
        y: item.Close
      }));

      const sellMarkers = optimizedData
      .filter(item => item.Signal === "SELL")
      .map(item => ({
        x: new Date(item.Date),
        y: item.Close
      }));

      // =========================
      // SET CHARTS
      // =========================
      setChartData({

        // CANDLE
        candlestickChart: {

          datasets: [
            {
              label: `${symbol} Candlestick`,
              data: candleData,
              parsing: false,
              borderColor: {
                up: "#00ff99",
                down: "#ff4444",
                unchanged: "#999"
              },
              color: {
                up: "#00ff99",
                down: "#ff4444",
                unchanged: "#999"
              },
              barThickness: 8,
              maxBarThickness: 10
            },
            {
              type: "scatter",
              label: "BUY",
              data: buyMarkers,
              backgroundColor: "#00ff99",
              borderColor: "#00ff99",
              pointRadius: 8,
              pointHoverRadius: 10
            },
            {
              type: "scatter",
              label: "SELL",
              data: sellMarkers,
              backgroundColor: "#ff4444",
              borderColor: "#ff4444",
              pointRadius: 8,
              pointHoverRadius: 10
            }
          ]
        },

        // PRICE
        priceChart: {

        labels: labels,

          datasets: [

            {
              label: `${symbol} Price`,
              data: prices,
              borderColor: "#00ff99",
              backgroundColor: "rgba(0,255,153,0.2)",
              tension: 0.4,
              pointRadius: 3
            },

            {
              label: "SMA 5",
              data: sma,
              borderColor: "#ffcc00",
              backgroundColor: "rgba(255,204,0,0.2)",
              tension: 0.4,
              pointRadius: 2
            },

            {
              label: "BB Upper",
              data: bbUpper,
              borderColor: "#ff00ff",
              backgroundColor: "transparent",
              tension: 0.4,
              pointRadius: 0
            },
            {
              label: "BB Middle",
              data: bbMiddle,
              borderColor: "#00bfff",
              backgroundColor: "transparent",
              tension: 0.4,
              pointRadius: 0
            },
            {
              label: "BB Lower",
              data: bbLower,
              borderColor: "#ff6600",
              backgroundColor: "transparent",
              tension: 0.4,
              pointRadius: 0
            },


          ],
        
        },

        // RSI
        rsiChart: {

          labels: labels,

          datasets: [

            {
              label: "RSI",
              data: rsi,
              borderColor: "#ff4444",
              backgroundColor: "rgba(255,68,68,0.2)",
              tension: 0.4,
              pointRadius: 2
            }
          ]
        },

        // MACD
        macdChart: {

          labels: labels,

          datasets: [

            {
              label: "MACD",
              data: macd,
              borderColor: "#00bfff",
              backgroundColor: "rgba(0,191,255,0.2)",
              tension: 0.4,
              pointRadius: 2
            },

            {
              label: "Signal Line",
              data: signalLine,
              borderColor: "#ff66cc",
              backgroundColor: "rgba(255,102,204,0.2)",
              tension: 0.4,
              pointRadius: 2
            }
          ]
        },
        volumeChart: {
          labels: labels,
          datasets: [
            {
              label: "Volume",
              data: volume,
              backgroundColor:
              "rgba(0,191,255,0.5)",
              borderColor: "#00bfff",
              borderWidth: 1
            }
          ]
        }

      });

    } catch (error) {

      console.log(
        "Error fetching data",
        error
      );
    }
  };

  // =========================
  // AUTO REFRESH
  // =========================
  useEffect(() => {

    if(symbol !== ""){
      fetchData();
    }

    const interval = setInterval(() => {

      if(symbol !== ""){
        fetchData();
      }

    }, 5000);

    return () => clearInterval(interval);

  }, [symbol, timeframe, selectedModel]);

  return (

    <>

    {/* LIVE TICKER BAR */}

<div
  style={{
    width: "100%",
    overflow: "hidden",
    background: "#111827",
    padding: "12px 0",
    borderBottom: "1px solid #334155"
  }}
>

  <marquee
    behavior="scroll"
    direction="left"
    scrollamount="8"
  >

    {tickerData.map((stock, index) => (

      <span
        key={index}
        style={{
          marginRight: "50px",
          color:
            stock.change < 0
              ? "#ef4444"
              : "#22c55e",
          fontWeight: "bold",
          fontSize: "18px"
        }}
      >

        {stock.symbol}

        {"  ₹"}

        {stock.price}

        {"  "}

        {stock.change > 0 ? "▲" : "▼"}

        {" "}

        {stock.change}%

      </span>
    ))}

  </marquee>

</div>

    <div
      style={{
        backgroundColor: "#0f172a",
        minHeight: "100vh",
        color: "white",
        padding: "30px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center"
      }}
    >

      {/* TITLE */}
      <h1
      style={{
        fontSize: "60px",
        marginBottom: "35px",
        textAlign: "center"
      }}
      >
       NSE STOCK PREDICTOR
      </h1>

      <p
        style={{
          color: "#94a3b8",
          marginBottom: "25px",
          fontSize: "18px"
        }}
      >
      {new Date().toLocaleString()}
      </p>

      {/* INPUT */}
      <div style={{ marginBottom: "30px" }}>

        <input
          value={symbol}

          onChange={(e) =>
            setSymbol(e.target.value)
          }

          placeholder="Enter Stock Symbol"

          style={{
            padding: "12px",
            marginRight: "10px",
            borderRadius: "5px",
            border: "none",
            width: "250px",
            fontSize: "16px"
          }}
        />

        <button

          onClick={fetchData}

          style={{
            padding: "12px 20px",
            borderRadius: "5px",
            cursor: "pointer",
            border: "none",
            background: "#00ff99",
            fontWeight: "bold",
            fontSize: "16px"
          }}
        >
          Load Chart
        </button>
      </div>

      {/* TIMEFRAME BUTTONS */}
      <div
      style={{
        display: "flex",
        gap: "10px",
        marginTop: "10px",
        marginBottom: "20px",
        flexWrap: "wrap",
        justifyContent: "center"
        }}
      >

  {[
    "1M",
    "5M",
    "15M",
    "1H",
    "1D",
    "1W",
    "1MO",
    "5Y"
  ].map((tf) => (

    <button

      key={tf}

      onClick={() =>
        setTimeframe(tf)
      }

      style={{

        padding: "10px 18px",

        borderRadius: "8px",

        border:
          timeframe === tf
            ? "2px solid #00E396"
            : "1px solid gray",

        background:
          timeframe === tf
            ? "#065f46"
            : "#1f2937",

        color: "white",

        cursor: "pointer",

        fontWeight: "bold"
      }}
             >

          {tf}

          </button>
        ))}
      </div>

     {/* MARKET STATUS */}

      <div
      style={{
        marginBottom: "15px",
        fontWeight: "bold",
        fontSize: "20px",
        color: market.color
      }}
      >
      {market.status}
      </div>

      {/* MARKET OVERVIEW */}

{marketOverview && (

  <div
    style={{
      marginBottom: "25px",
      textAlign: "center"
    }}
  >

    <h2
      style={{
        color:
          marketOverview.trend ===
          "BULLISH"
            ? "#22c55e"
            : "#ef4444"
      }}
    >
      Market Trend:
      {" "}
      {marketOverview.trend}
    </h2>

    <p
      style={{
        color: "#00ff99"
      }}
    >
      Top Gainer:
      {" "}
      {
        marketOverview.top_gainer
          ?.symbol
      }

      {" ("}

      {
        marketOverview.top_gainer
          ?.change
      }

      %)
    </p>

    <p
      style={{
        color: "#ff4444"
      }}
    >
      Top Loser:
      {" "}
      {
        marketOverview.top_loser
          ?.symbol
      }

      {" ("}

      {
        marketOverview.top_loser
          ?.change
      }

      %)
    </p>

  </div>
)}

{/* NIFTY 50 LIVE */}

<div
  style={{
    width: "95%",
    maxWidth: "1100px",
    marginTop: "25px",
    marginBottom: "25px"
  }}
>
  <NiftyChart />
</div>


      {/* SIGNAL */}
      <h2>

        Signal:{" "}

        <span
          style={{
            color:
              signal === "BUY"
                ? "#00ff99"
                : signal === "SELL"
                ? "#ff4444"
                : "#ffcc00"
          }}
        >
          {signal}
        </span>
      </h2>

      {/* RECOMMENDATION */}
      <h2
        style={{
          marginTop: "10px",
          color: "#38bdf8"
        }}
      >
        AI Recommendation: {recommendation}
      </h2>

      {/* ===================================== */}
      {/* AI PREDICTION CARD */}
      {/* ===================================== */}
      {
      prediction && (
      <div
      style={{
        background: "#1e293b",
        padding: "20px",
        borderRadius: "15px",
        marginTop: "20px",
        color: "white",
        textAlign: "center",
        boxShadow: "0 0 15px rgba(0,0,0,0.3)"
      }}
      >
        <h2 style={{ color: "#38bdf8" }}>
          AI Tomorrow Prediction
          </h2>
          <h3>
            Current Price:
            {" "}
            ₹{prediction.current_price}
            </h3>
            <h3>
              Predicted Price:
              {" "}
              ₹{prediction.predicted_price}
              </h3>
              <h2
              style={{
                color:
                prediction.trend === "BULLISH"
                ? "#22c55e"
                : "#ef4444"
              }}
              >
                {prediction.trend === "BULLISH"
                ? "📈 BULLISH"
                : "📉 BEARISH"}
                </h2>
                </div>
              )
            }

      {/* MODEL SELECTION */}

<div
  style={{
    display: "flex",
    gap: "15px",
    marginTop: "25px",
    marginBottom: "15px",
    justifyContent: "center",
    flexWrap: "wrap"
  }}
>

  <button

    onClick={() =>
      setSelectedModel("xgboost")
    }

    style={{

      padding: "12px 24px",

      borderRadius: "10px",

      border: "none",

      cursor: "pointer",

      background:
        selectedModel === "xgboost"
          ? "#00E396"
          : "#334155",

      color: "white",

      fontWeight: "bold",

      fontSize: "15px",

      transition: "0.3s"
    }}
  >
    XGBoost
  </button>

  <button

    onClick={() =>
      setSelectedModel("catboost")
    }

    style={{

      padding: "12px 24px",

      borderRadius: "10px",

      border: "none",

      cursor: "pointer",

      background:
        selectedModel === "catboost"
          ? "#ff00ff"
          : "#334155",

      color: "white",

      fontWeight: "bold",

      fontSize: "15px",

      transition: "0.3s"
    }}
  >
    CatBoost
  </button>

</div>
      {/* ================================= */}
      {/* INTRADAY AI FORECAST */}
      {/* ================================= */}
      {intradayPrediction && (

  <div
    style={{
      background: "#1e293b",
      padding: "20px",
      borderRadius: "15px",
      marginTop: "20px",
      color: "white",
      textAlign: "center",
      boxShadow: "0 0 15px rgba(0,0,0,0.3)"
    }}
  >

    <h2 style={{ color: "#38bdf8" }}>
   AI Intraday Forecast
</h2>

<h3
  style={{
    color:
      selectedModel === "xgboost"
        ? "#00E396"
        : "#ff00ff",

    marginTop: "10px"
  }}
>
  Active Model:
  {" "}
  {selectedModel.toUpperCase()}
</h3>

    <h3>
      Current Price:
      ₹{intradayPrediction.current_price}
    </h3>

    <h3>
      Market Close Prediction:
      ₹{intradayPrediction.market_close_prediction}
    </h3>

    <h3>
      Trend:
      <span
        style={{
          color:
            intradayPrediction.trend === "BULLISH"
              ? "#22c55e"
              : "#ef4444"
        }}
      >
        {" "}
        {intradayPrediction.trend}
      </span>
    </h3>

    <h3>
      Confidence:
      {intradayPrediction.confidence}
    </h3>

  </div>

)}

{
intradayPrediction?.session_forecast?.length > 0 && (

<div
  style={{
    width: "95%",
    maxWidth: "1100px",
    margin: "25px auto"
  }}
>

  <ForecastChart

    currentPrice={
      intradayPrediction.current_price
    }

    forecast={
      intradayPrediction.session_forecast
    }

  />

</div>

)}
      {/* CONFIDENCE SCORE */}
      <div
        style={{
          marginTop: "20px",
          width: "400px"
      }}
      >

      <h3>
        AI Confidence Score:
        <span
        style={{
          marginLeft: "10px",
          color:
          confidence > 80
          ? "#00ff99"
          : confidence > 60
          ? "#ffcc00"
          : "#ff4444"
        }}
        >
          {confidence}%
          </span>
          </h3>
          {/* BAR */}
          <div
          style={{
            width: "100%",
            height: "20px",
            background: "#334155",
            borderRadius: "10px",
            overflow: "hidden"
          }}
          >
            <div
            style={{
              width: `${confidence}%`,
              height: "100%",
              background:
              confidence > 80
              ? "#00ff99"
              : confidence > 60
              ? "#ffcc00"
              : "#ff4444",
              transition: "0.5s"
            }}
            />
            </div>
            </div>

      {/* METRICS */}
      {metrics && (

        <div
          style={{
            display: "flex",
            gap: "20px",
            flexWrap: "wrap",
            marginTop: "30px",
            justifyContent: "center"
          }}
        >

          <div style={cardStyle}>
            <h3>Price</h3>
            <p>₹ {metrics.price?.toFixed(2)}</p>
          </div>

          <div style={cardStyle}>
            <h3>SMA 5</h3>
            <p>{metrics.sma?.toFixed(2)}</p>
          </div>

          <div style={cardStyle}>
            <h3>RSI</h3>
            <p>{metrics.rsi?.toFixed(2)}</p>
          </div>

          <div style={cardStyle}>
            <h3>Sentiment</h3>
            <p>{sentiment}</p>
          </div>

        </div>
      )}

      {/* CANDLESTICK */}
      {chartData && (

        <div
          style={{
            marginTop: "40px",
            width: "95%",
            maxWidth: "1100px",
            height: "600px",
            background: "#1e293b",
            padding: "20px",
            borderRadius: "10px"
          }}
        >

          <h2>Candlestick Chart</h2>

          <Chart
            type="candlestick"
            data={chartData.candlestickChart}
            options={candleOptions}
          />
        </div>
      )}

      {/* PRICE CHART */}

      {chartData && (

      <div
        style={{
          marginTop: "40px",
          width: "95%",
          maxWidth: "1100px",
          background: "#1e293b",
          padding: "20px",
          borderRadius: "10px"
        }}
      >

      <h2>Price & SMA</h2>

      <div
        style={{
          height: "500px"
        }}
      >

        <Line
  data={chartData.priceChart}
  options={options}
/>

      </div>

    </div>

  )}

      {/* RSI */}
      {chartData && (

        <div
          style={{
            marginTop: "40px",
            width: "95%",
            maxWidth: "1100px",
            background: "#1e293b",
            padding: "20px",
            borderRadius: "10px"
          }}
        >

          <h2>RSI Indicator</h2>

          <div
            style={{
              height: "250px"
          }}
        >

          <Line
            data={chartData.rsiChart}
            options={options}
          />
        </div>
        </div>
      )}

      {/* MACD */}
      {chartData && (

        <div
          style={{
            marginTop: "40px",
            width: "95%",
            maxWidth: "1100px",
            background: "#1e293b",
            padding: "20px",
            borderRadius: "10px"
          }}
        >

          <h2>MACD Indicator</h2>

          <div
          style={{
            height: "250px"
          }}
        >

          <Line
            data={chartData.macdChart}
            options={options}
          />
        </div>
        </div>
      )}

      {/* VOLUME */}
      {chartData && (
        <div
        style={{
          marginTop: "40px",
          width: "95%",
          maxWidth: "1100px",
          background: "#1e293b",
          padding: "20px",
          borderRadius: "10px"
        }}
        >
          <h2>Volume Analysis</h2>

          <div
           style={{
            height: "250px"
          }}
          >
          <Chart
          type="bar"
          data={chartData.volumeChart}
          options={options}
          />
          </div>
        </div>
        )}

      {/* NEWS */}
      <div
        style={{
          marginTop: "40px",
          width: "95%",
          maxWidth: "1100px",
          background: "#1e293b",
          padding: "20px",
          borderRadius: "10px",
          marginBottom: "50px"
        }}
      >

        <h2>📰 Latest News</h2>

        {news.map((item, index) => (

          <div
            key={index}
            style={{
              marginBottom: "20px",
              padding: "10px",
              borderBottom:
                "1px solid rgba(255,255,255,0.1)"
            }}
          >

            <h4>{item.title}</h4>

            <p>
              Sentiment:
              <span
                style={{
                  marginLeft: "10px",
                  color:
                    item.sentiment.includes("POSITIVE")
                      ? "#00ff99"
                      : item.sentiment.includes("NEGATIVE")
                      ? "#ff4444"
                      : "#ffcc00"
                }}
              >
                {item.sentiment}
              </span>
            </p>

          </div>
        ))}

      </div>

<footer
style={{
  textAlign:"center",
  padding:"20px",
  color:"#94a3b8"
}}
>

AI-Powered Real-Time Stock Market Prediction & Analysis System

</footer>
    </div>
    </>
  );
}



export default App;