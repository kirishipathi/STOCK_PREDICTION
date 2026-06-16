# AI-Powered Real-Time Stock Market Prediction and Analysis System

## Overview

An end-to-end AI-powered stock market analytics platform that combines real-time market monitoring, technical analysis, machine learning forecasting, and interactive financial visualization.

The system provides:

- Real-time stock tracking
- NIFTY 50 live market monitoring
- Technical indicator analysis
- AI-based tomorrow price prediction
- Intraday forecasting engine
- Buy / Sell / Hold recommendations
- Interactive financial dashboards

---

## Key Features

### Real-Time Market Analytics
- Live stock price monitoring
- NIFTY 50 live chart visualization
- Market overview dashboard
- Auto-refreshing market data

### Technical Analysis
- RSI (Relative Strength Index)
- MACD
- SMA (Simple Moving Average)
- EMA 20
- EMA 50
- VWAP
- Momentum
- Volatility

### AI Prediction Engine
- Tomorrow price forecasting
- Intraday multi-step forecasting
- Trend analysis
- Confidence estimation
- Recommendation generation

### Interactive Dashboard
- React-based frontend
- Dynamic charts and visualizations
- Responsive design
- Real-time API integration

---

## System Architecture

```
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI Backend
 │
 ├──────── Yahoo Finance API
 │
 ├──────── Technical Indicator Engine
 │
 ├──────── Tomorrow Prediction Model
 │
 └──────── XGBoost Intraday Forecast Model
          │
          ▼
     Prediction Results
          │
          ▼
     Dashboard Visualization
```

---

## Technology Stack

### Frontend
- ReactJS
- Chart.js
- Axios
- CSS

### Backend
- FastAPI
- Python

### Machine Learning
- XGBoost
- Scikit-Learn
- NumPy
- Pandas

### Data Source
- Yahoo Finance API

---

## Dataset Information

| Metric | Value |
|----------|----------|
| Training Samples | 193,384 |
| Features | 14 |
| Input Sequence | 60 Candles |
| Forecast Horizon | 72 Candles |
| Stocks Covered | 50 NSE Stocks |
| Interval | 5 Minutes |

---

## Engineered Features

The model uses 14 engineered market features:

- Open
- High
- Low
- Close
- Volume
- SMA 5
- EMA 20
- EMA 50
- RSI
- MACD
- Signal Line
- Volatility
- Momentum
- VWAP

---

## Machine Learning Model

### Intraday Forecast Model

Model:
- XGBoost MultiOutput Regressor

Objective:
- Predict future market movement for the remaining trading session

Performance:

| Metric | Value |
|----------|----------|
| MAE | 0.00132 |
| Training Time | 47.99 Minutes |
| Forecast Horizon | 72 Future Candles |

---

## Project Workflow

### Data Collection

- Download NSE stock data
- Collect 5-minute interval market candles
- Store historical market data

### Feature Engineering

- Calculate technical indicators
- Generate momentum and volatility features
- Normalize feature space

### Model Training

- Train XGBoost MultiOutput Regressor
- Evaluate model performance
- Save trained model

### Prediction

- Generate tomorrow forecast
- Generate intraday forecast
- Produce Buy / Sell / Hold recommendation

### Visualization

- Display live charts
- Display AI predictions
- Display market analytics

---

## API Endpoints

### Live Stock Data

```
GET /stock/{symbol}
```

### Tomorrow Prediction

```
GET /predict/{symbol}
```

### Intraday Prediction

```
GET /intraday_predict/{symbol}
```

### Market Overview

```
GET /market_overview
```

### NIFTY 50 Live Data

```
GET /nifty_live
```

---

## Dashboard Modules

### NIFTY 50 Live Market
- Live index tracking
- Interactive line chart
- High / Low / Current values

### Market Overview
- Top Gainers
- Top Losers
- Market Sentiment

### Tomorrow Prediction
- Predicted closing price
- Expected trend
- Confidence estimation

### Intraday Forecast
- Multi-step forecasting
- Forecast path visualization

### Recommendation Engine
- BUY
- SELL
- HOLD

---

## Future Enhancements

- Transformer-based forecasting models
- Reinforcement learning strategies
- Portfolio optimization
- Risk management engine
- Real-time WebSocket streaming
- Cloud deployment
- Mobile application support

---

## Project Outcome

Successfully developed an AI-powered financial analytics platform capable of:

- Real-time stock monitoring
- Technical market analysis
- Intraday forecasting
- Tomorrow price prediction
- Decision support recommendations
- Interactive dashboard visualization

The system demonstrates the integration of Financial Analytics, Machine Learning, Data Engineering, and Full Stack Development into a unified stock market intelligence platform.

---

## Author

Jeevanantham C

B.Tech Artificial Intelligence and Machine Learning

Project: AI-Powered Real-Time Stock Market Prediction and Analysis System# NSE-STOCK-PREDICTION
