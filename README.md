<div align="center">

# 📈 NSE Stock Prediction AI

### 🤖 AI-Powered Real-Time Stock Market Prediction and Analysis System

**An end-to-end financial analytics platform combining real-time market monitoring, technical analysis, machine learning forecasting, and interactive visualization.**

![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-ML_Model-EB5E28?style=for-the-badge&logo=xgboost&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

</div>

<br>

## 📌 Overview

**NSE Stock Prediction AI** is an end-to-end AI-powered stock market analytics platform that combines **real-time market monitoring**, **technical analysis**, **machine learning forecasting**, and **interactive financial visualization**.

The system provides:

- 📡 Real-time stock tracking
- 📊 NIFTY 50 live market monitoring
- 📐 Technical indicator analysis
- 🔮 AI-based tomorrow price prediction
- ⏱️ Intraday forecasting engine
- 🟢🔴 Buy / Sell / Hold recommendations
- 🖥️ Interactive financial dashboards

<br>

---

## ✨ Key Features

### 1️⃣ 📡 Real-Time Market Analytics

- 💹 Live stock price monitoring
- 📈 NIFTY 50 live chart visualization
- 🗂️ Market overview dashboard
- 🔄 Auto-refreshing market data

<br>

### 2️⃣ 📐 Technical Analysis

| | | |
|---|---|---|
| **RSI** | **MACD** | **SMA** |
| **EMA 20** | **EMA 50** | **VWAP** |
| **Momentum** | **Volatility** | |

<br>

### 3️⃣ 🔮 AI Prediction Engine

- 🌅 Tomorrow price forecasting
- ⏱️ Intraday multi-step forecasting
- 📊 Trend analysis
- 🎯 Confidence estimation
- 🟢🔴 Recommendation generation

<br>

### 4️⃣ 🖥️ Interactive Dashboard

- ⚛️ React-based frontend
- 📊 Dynamic charts and visualizations
- 📱 Responsive design
- 🔌 Real-time API integration

<br>

---

## 🏗️ System Architecture
            ┌──────────────────────────┐
            │        🧍 User            │
            └─────────────┬────────────┘
                          │
                          ▼
            ┌──────────────────────────┐
            │     ⚛️ React Frontend      │
            └─────────────┬────────────┘
                          │
                          ▼
            ┌──────────────────────────┐
            │    🐍 FastAPI Backend     │
            └─────────────┬────────────┘
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                      │
    ▼                     ▼                      ▼
┌───────────────┐   ┌──────────────────┐   ┌─────────────────────┐

│ 📡 Yahoo       │   │ 📐 Technical      │   │ 🔮 Tomorrow          │

│ Finance API    │   │ Indicator Engine │   │ Prediction Model     │

└───────────────┘   └──────────────────┘   └─────────────────────┘

│

▼

┌─────────────────────────┐

│ ⚡ XGBoost Intraday       │

│ Forecast Model            │

└─────────────┬───────────┘

│

▼

┌─────────────────────────┐

│   📊 Prediction Results  │

└─────────────┬───────────┘

│

▼

┌─────────────────────────┐

│ 🖥️ Dashboard Visualization│

└─────────────────────────┘

<br>

---

## 🧰 Tech Stack

<div align="center">

| Layer | Technology |
|:---:|:---:|
| 🎨 **Frontend** | ReactJS, Chart.js, Axios, CSS |
| 🐍 **Backend** | FastAPI, Python |
| 🤖 **Machine Learning** | XGBoost, Scikit-Learn, NumPy, Pandas |
| 📡 **Data Source** | Yahoo Finance API |

</div>

<br>

---

## 📊 Dataset Information

<div align="center">

| Metric | Value |
|:---:|:---:|
| **Training Samples** | 193,384 |
| **Features** | 14 |
| **Input Sequence** | 60 Candles |
| **Forecast Horizon** | 72 Candles |
| **Stocks Covered** | 50 NSE Stocks |
| **Interval** | 5 Minutes |

</div>

<br>

### 🧬 Engineered Features

The model uses **14 engineered market features**:

| | | |
|---|---|---|
| Open | High | Low |
| Close | Volume | SMA 5 |
| EMA 20 | EMA 50 | RSI |
| MACD | Signal Line | Volatility |
| Momentum | VWAP | |

<br>

---

## 🤖 Machine Learning Model

<div align="center">

### Intraday Forecast Model

**Model:** XGBoost MultiOutput Regressor
**Objective:** Predict future market movement for the remaining trading session

</div>

<br>

<div align="center">

| Metric | Value |
|:---:|:---:|
| **MAE** | 0.00132 |
| **Training Time** | 47.99 Minutes |
| **Forecast Horizon** | 72 Future Candles |

</div>

<br>

---

## 🔄 Project Workflow

**1️⃣ Data Collection**
- 📥 Download NSE stock data
- ⏱️ Collect 5-minute interval market candles
- 🗄️ Store historical market data

**2️⃣ Feature Engineering**
- 📐 Calculate technical indicators
- 📊 Generate momentum and volatility features
- ⚖️ Normalize feature space

**3️⃣ Model Training**
- 🤖 Train XGBoost MultiOutput Regressor
- ✅ Evaluate model performance
- 💾 Save trained model

**4️⃣ Prediction**
- 🌅 Generate tomorrow forecast
- ⏱️ Generate intraday forecast
- 🟢🔴 Produce Buy / Sell / Hold recommendation

**5️⃣ Visualization**
- 📈 Display live charts
- 🔮 Display AI predictions
- 📊 Display market analytics

<br>

---

## 📡 API Endpoints

| Endpoint | Description |
|---|---|
| `GET /stock/{symbol}` | 💹 Live Stock Data |
| `GET /predict/{symbol}` | 🌅 Tomorrow Prediction |
| `GET /intraday_predict/{symbol}` | ⏱️ Intraday Prediction |
| `GET /market_overview` | 🗂️ Market Overview |
| `GET /nifty_live` | 📈 NIFTY 50 Live Data |

<br>

---

## 🖥️ Dashboard Modules

| | Module | Highlights |
|---|---|---|
| 📊 | **NIFTY 50 Live Market** | Live index tracking, interactive line chart, High / Low / Current values |
| 🗂️ | **Market Overview** | Top Gainers, Top Losers, Market Sentiment |
| 🌅 | **Tomorrow Prediction** | Predicted closing price, expected trend, confidence estimation |
| ⏱️ | **Intraday Forecast** | Multi-step forecasting, forecast path visualization |
| 🟢🔴 | **Recommendation Engine** | BUY · SELL · HOLD |

<br>

---

## 🔮 Future Enhancements

- 🧠 Transformer-based forecasting models
- 🎮 Reinforcement learning strategies
- 📊 Portfolio optimization
- ⚠️ Risk management engine
- 🔌 Real-time WebSocket streaming
- ☁️ Cloud deployment
- 📱 Mobile application support

<br>

---

<div align="center">

## 🎯 Project Outcome

</div>

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
