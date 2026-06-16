from unittest import signals

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from tensorflow.keras.models import load_model
import sqlite3
import pandas as pd

import numpy as np
import yfinance as yf
import joblib


# Sentiment Imports
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
import os

from preprocess import X_test

# =========================
# ENVIRONMENT VARIABLES
# =========================
load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

# =========================
# NEWS + NLP
# =========================
newsapi = NewsApiClient(api_key=API_KEY)

analyzer = SentimentIntensityAnalyzer()

# =========================
# STOCK NAME MAPPING
# =========================
company_map = {

    "RELIANCE": "Reliance Industries",
    "TCS": "Tata Consultancy Services",
    "INFY": "Infosys",
    "HDFCBANK": "HDFC Bank",
    "ICICIBANK": "ICICI Bank",
    "SBIN": "State Bank of India",
    "ITC": "ITC Limited",
    "LT": "Larsen and Toubro",
    "KOTAKBANK": "Kotak Mahindra Bank",
    "AXISBANK": "Axis Bank",
    "TATAMOTORS": "Tata Motors",
    "TATASTEEL": "Tata Steel",
    "MARUTI": "Maruti Suzuki",
    "SUNPHARMA": "Sun Pharmaceutical",
    "BAJFINANCE": "Bajaj Finance",
    "WIPRO": "Wipro",
    "TECHM": "Tech Mahindra",
    "ULTRACEMCO": "UltraTech Cement",
    "NTPC": "NTPC",
    "POWERGRID": "Power Grid Corporation",
    "ONGC": "ONGC",
    "BHARTIARTL": "Bharti Airtel",
    "ASIANPAINT": "Asian Paints",
    "HINDUNILVR": "Hindustan Unilever",
    "TITAN": "Titan Company",
    "NESTLEIND": "Nestle India",
    "ADANIPORTS": "Adani Ports",
    "ADANIENT": "Adani Enterprises",
    "JSWSTEEL": "JSW Steel",
    "HCLTECH": "HCL Technologies"
}

# =========================
# FASTAPI APP
# =========================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================
# LOAD AI MODEL
# =====================================
model = load_model("stock_lstm_model.h5")

scaler = joblib.load("scaler.save")

# =====================================
# LOAD INTRADAY MODEL
# =====================================

intraday_model = joblib.load(
    "xgboost_intraday_model.pkl"
)

catboost_model = joblib.load(
    "catboost_intraday_model.pkl"
)

intraday_scaler = joblib.load(
    "intraday_scaler.save"
)

# =========================================================
# BASIC STOCK DATA
# =========================================================
@app.get("/stock/{symbol}")
def get_stock(symbol: str):

    conn = sqlite3.connect("stocks.db")

    query = f"""
    SELECT * FROM stocks
    WHERE Stock LIKE '{symbol.upper()}%'
    """

    df = pd.read_sql(query, conn)

    return df.to_dict(orient="records")


# =========================================================
# LATEST PRICE
# =========================================================
@app.get("/latest/{symbol}")
def latest_price(symbol: str):

    conn = sqlite3.connect("stocks.db")

    query = f"""
    SELECT * FROM stocks
    WHERE Stock LIKE '{symbol.upper()}%'
    ORDER BY Date DESC LIMIT 1
    """

    df = pd.read_sql(query, conn)

    return df.to_dict(orient="records")


# =========================================================
# SMA ENDPOINT
# =========================================================
@app.get("/sma/{symbol}")
def sma(symbol: str):

    conn = sqlite3.connect("stocks.db")

    query = f"""
    SELECT * FROM stocks
    WHERE Stock LIKE '{symbol.upper()}%'
    """

    df = pd.read_sql(query, conn)

    df["SMA_5"] = df["Close"].rolling(5).mean()

    df = df.fillna(0)

    return df.tail(10).to_dict(orient="records")


# =========================================================
# PRICE CHANGE
# =========================================================
@app.get("/change/{symbol}")
def price_change(symbol: str):

    conn = sqlite3.connect("stocks.db")

    query = f"""
    SELECT * FROM stocks
    WHERE Stock LIKE '{symbol.upper()}%'
    ORDER BY Date DESC LIMIT 2
    """

    df = pd.read_sql(query, conn)

    latest = df.iloc[0]["Close"]
    previous = df.iloc[1]["Close"]

    change = latest - previous
    percent = (change / previous) * 100

    return {
        "latest": latest,
        "change": change,
        "percent": percent
    }


# =========================================================
# MAIN CHART + INDICATORS
# =========================================================
@app.get("/chart/{symbol}")
def chart_data(

    symbol: str,

    timeframe: str = "1D"
):

    # =================================
    # FORMAT SYMBOL
    # =================================
    symbol = symbol.upper()

    if ".NS" not in symbol:
        symbol += ".NS"

    # =================================
    # TIMEFRAME MAP
    # =================================
    timeframe_map = {

        "1M": {

            "period": "1d",

            "interval": "1m"
        },

        "5M": {

            "period": "5d",

            "interval": "5m"
        },

        "15M": {

            "period": "5d",

            "interval": "15m"
        },

        "1H": {

            "period": "1mo",

            "interval": "1h"
        },

        "1D": {

            "period": "6mo",

            "interval": "1d"
        },

        "1W": {

            "period": "5y",

            "interval": "1wk"
        },

        "1MO": {

            "period": "10y",

            "interval": "1mo"
        },

        "5Y": {

            "period": "5y",

            "interval": "1mo"
        }
    }

    # =================================
    # GET SETTINGS
    # =================================
    settings = timeframe_map.get(

        timeframe,

        timeframe_map["1D"]
    )

    # =================================
    # LIVE DOWNLOAD
    # =================================
    df = yf.download(

        symbol,

        period=settings["period"],

        interval=settings["interval"],

        auto_adjust=False
    )

    # =================================
    # EMPTY CHECK
    # =================================
    if df.empty:

        return {
        "error": "No data found"
        }

    # =================================
    # FIX MULTI INDEX
    # =================================
    if isinstance(df.columns, pd.MultiIndex):

        df.columns = (
            df.columns
            .get_level_values(0)
        )

    # =================================
    # RESET INDEX
    # =================================
    df.reset_index(inplace=True)

    # =========================
    # SMA Calculation
    # =========================
    df["SMA_5"] = df["Close"].rolling(5).mean()

    # =========================
    # BOLLINGER BANDS
    # =========================
    df["BB_Middle"] = (
        df["Close"]
        .rolling(window=20)
        .mean()
    )

    std_dev = (
        df["Close"]
        .rolling(window=20)
        .std()
    )

    df["BB_Upper"] = (
        df["BB_Middle"]
        + (std_dev * 2)
    )

    df["BB_Lower"] = (
        df["BB_Middle"]
        - (std_dev * 2)
    )

    # =========================
    # RSI Calculation
    # =========================
    delta = df["Close"].diff()

    gain = delta.where(delta > 0, 0)

    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()

    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = 100 - (100 / (1 + rs))

    # =========================
    # MACD Calculation
    # =========================
    short_ema = df["Close"].ewm(
        span=12,
        adjust=False
    ).mean()

    long_ema = df["Close"].ewm(
        span=26,
        adjust=False
    ).mean()

    df["MACD"] = short_ema - long_ema

    df["Signal_Line"] = df["MACD"].ewm(
        span=9,
        adjust=False
    ).mean()

    # =========================
    # REMOVE NaN ROWS
    # =========================
    df = df.dropna().reset_index(drop=True)
    # =========================
    # BUY / SELL SIGNALS
    # =========================
    if df.empty:
        signal = "HOLD"
        df["Signal"] = []
    else:
        signals = []
        
        for rsi in df["RSI"]:
            if rsi > 70:
                signals.append("SELL")
            elif rsi < 30:
                signals.append("BUY")
            else:
                signals.append("HOLD")
        df["Signal"] = signals
        signal = df["Signal"].iloc[-1]

    # =========================
    # LATEST METRICS
    # =========================
    latest_close = df["Close"].iloc[-1]

    latest_sma = df["SMA_5"].iloc[-1]

    latest_rsi = df["RSI"].iloc[-1]

    latest_macd = df["MACD"].iloc[-1]

    # =========================
    # DATE FIX
    # =========================

    if "Datetime" in df.columns:

        df["Date"] = (
            df["Datetime"]
            .astype(str)
        )

    elif "Date" in df.columns:

        df["Date"] = (
            df["Date"]
            .astype(str)
        )

    # =========================
    # CLEAN DATA
    # =========================
    df = df.replace(
        [np.inf, -np.inf],
        np.nan
    )

    df = df.dropna().reset_index(drop=True)

    # =========================
    # CHART DATA FORMAT
    # =========================
    chart_records = []

    for _, row in df.iterrows():

        chart_records.append({

            "Date": row["Date"],

            "Open": round(
                float(row["Open"]),
                2
            ),

            "High": round(
                float(row["High"]),
                2
            ),

            "Low": round(
                float(row["Low"]),
                2
            ),

            "Close": round(
                float(row["Close"]),
                2
            ),

            "Volume": round(
                float(row["Volume"]),
                2
            ),

            "SMA_5": round(
                float(row["SMA_5"]),
                2
            ),

            "RSI": round(
                float(row["RSI"]),
                2
            ),

            "MACD": round(
                float(row["MACD"]),
                2
            ),

            "Signal_Line": round(
                float(row["Signal_Line"]),
                2
            ),

            "BB_Upper": round(
                float(row["BB_Upper"]),
                2
            ),

            "BB_Middle": round(
                float(row["BB_Middle"]),
                2
            ),

            "BB_Lower": round(
                float(row["BB_Lower"]),
                2
            ),

            "Signal": row["Signal"]
        })

    # =========================
    # FINAL RESPONSE
    # =========================
    return {

        "chart": chart_records,

        "metrics": {

            "price": round(
                float(latest_close),
                2
            ),

            "sma": round(
                float(latest_sma),
                2
            ),

            "rsi": round(
                float(latest_rsi),
                2
            ),

            "macd": round(
                float(latest_macd),
                2
            ),

            "signal": signal
        }
    }
# =========================================================
# SENTIMENT ANALYSIS API
# =========================================================
@app.get("/sentiment/{symbol}")
def sentiment(symbol: str):

    try:

        company = company_map.get(
            symbol.upper(),
            symbol
        )

        articles = newsapi.get_everything(
            q=company,
            language="en",
            sort_by="publishedAt",
            domains="economictimes.indiatimes.com,moneycontrol.com,business-standard.com",
            page_size=5
        )

        results = []

        overall_score = 0

        for article in articles["articles"]:

            title = article["title"]

            score = analyzer.polarity_scores(title)

            compound = score["compound"]

            overall_score += compound

            if compound > 0:
                sentiment_label = "POSITIVE "

            elif compound < 0:
                sentiment_label = "NEGATIVE "

            else:
                sentiment_label = "NEUTRAL "

            results.append({

                "title": title,

                "sentiment": sentiment_label,

                "score": compound
            })

        avg_score = overall_score / max(
            len(results),
            1
        )

        if avg_score > 0:
            overall = "POSITIVE "

        elif avg_score < 0:
            overall = "NEGATIVE "

        else:
            overall = "NEUTRAL "

        return {

            "overall_sentiment": overall,

            "news": results
        }

    except Exception as e:

        return {

            "overall_sentiment": "NEUTRAL ",

            "news": [

                {
                    "title":
                    "Unable to fetch news currently",

                    "sentiment":
                    "NEUTRAL ",

                    "score": 0
                }
            ],

            "error": str(e)
        }
@app.get("/recommendation/{symbol}")
def recommendation(symbol: str):

    # =========================
    # STOCK DATA
    # =========================
    conn = sqlite3.connect("stocks.db")

    query = f"""
    SELECT * FROM stocks
    WHERE Stock LIKE '{symbol.upper()}%'
    """

    df = pd.read_sql(query, conn)

    # =========================
    # RSI CALCULATION
    # =========================
    delta = df["Close"].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = 100 - (100 / (1 + rs))

    df = df.fillna(0)

    latest_rsi = df["RSI"].iloc[-1]

    # =========================
    # RSI SIGNAL
    # =========================
    if latest_rsi > 70:
        signal = "SELL"

    elif latest_rsi < 30:
        signal = "BUY"

    else:
        signal = "HOLD"

    # =========================
    # SENTIMENT
    # =========================
    company = company_map.get(
        symbol.upper(),
        symbol
    )

    articles = newsapi.get_everything(
        q=company,
        language="en",
        sort_by="publishedAt",
        domains="economictimes.indiatimes.com,moneycontrol.com,business-standard.com",
        page_size=5
    )

    overall_score = 0

    for article in articles["articles"]:

        title = article["title"]

        score = analyzer.polarity_scores(title)

        overall_score += score["compound"]

    avg_score = overall_score / max(
        len(articles["articles"]),
        1
    )

    # =========================
    # CONFIDENCE SCORE
    # =========================
    confidence = 50

    # RSI contribution
    if latest_rsi < 30:
        confidence += 20

    elif latest_rsi > 70:
        confidence += 20

    # Sentiment contribution
    if avg_score > 0.3:
        confidence += 20

    elif avg_score < -0.3:
        confidence += 20

    # MACD contribution
    short_ema = df["Close"].ewm(
        span=12,
        adjust=False
    ).mean()

    long_ema = df["Close"].ewm(
        span=26,
        adjust=False
    ).mean()

    macd = short_ema - long_ema

    signal_line = macd.ewm(
        span=9,
        adjust=False
    ).mean()

    latest_macd = macd.iloc[-1]

    latest_signal_line = signal_line.iloc[-1]

    if latest_macd > latest_signal_line:
        confidence += 10

    else:
        confidence += 5

    # LIMIT SCORE
    confidence = min(confidence, 100)

    # =========================
    # FINAL AI RECOMMENDATION
    # =========================
    if signal == "BUY" and avg_score > 0:
        final = "🔥 STRONG BUY"

    elif signal == "BUY":
        final = "⚠️ CAUTIOUS BUY"

    elif signal == "SELL" and avg_score < 0:
        final = "🔻 STRONG SELL"

    elif signal == "SELL":
        final = "⚠️ CAUTIOUS SELL"

    else:
        final = "😐 HOLD"

    return {

        "recommendation": final,

        "confidence": confidence,

        "rsi_signal": signal,

        "sentiment_score": avg_score
    }

# =========================================================
# AI PRICE PREDICTION
# =========================================================
@app.get("/predict/{symbol}")
def predict_price(symbol: str):

    # =====================================
    # FORMAT SYMBOL
    # =====================================
    if (
        ".NS" not in symbol
        and ".BO" not in symbol
    ):
        symbol += ".NS"

    # =====================================
    # DOWNLOAD DATA
    # =====================================
    df = yf.download(

        symbol,

        period="1y",

        interval="1d",

        auto_adjust=False
    )

    # =====================================
    # EMPTY CHECK
    # =====================================
    if df.empty:

        return {
            "error": "Invalid stock symbol"
        }

    # =====================================
    # FIX MULTI INDEX
    # =====================================
    if isinstance(df.columns, pd.MultiIndex):

        df.columns = (
            df.columns
            .get_level_values(0)
        )

    # =====================================
    # RESET INDEX
    # =====================================
    df.reset_index(inplace=True)

    # =====================================
    # SMA
    # =====================================
    df["SMA_5"] = (
        df["Close"]
        .rolling(window=5)
        .mean()
    )

    # =====================================
    # RSI
    # =====================================
    delta = df["Close"].diff()

    gain = delta.where(delta > 0, 0)

    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = (
        100 - (100 / (1 + rs))
    )

    # =====================================
    # MACD
    # =====================================
    short_ema = (
        df["Close"]
        .ewm(span=12, adjust=False)
        .mean()
    )

    long_ema = (
        df["Close"]
        .ewm(span=26, adjust=False)
        .mean()
    )

    df["MACD"] = (
        short_ema - long_ema
    )

    df["Signal_Line"] = (
        df["MACD"]
        .ewm(span=9, adjust=False)
        .mean()
    )

    # =====================================
    # BOLLINGER BANDS
    # =====================================
    df["BB_Middle"] = (
        df["Close"]
        .rolling(window=20)
        .mean()
    )

    std_dev = (
        df["Close"]
        .rolling(window=20)
        .std()
    )

    df["BB_Upper"] = (
        df["BB_Middle"]
        + (std_dev * 2)
    )

    df["BB_Lower"] = (
        df["BB_Middle"]
        - (std_dev * 2)
    )

    # =====================================
    # HANDLE NaN
    # =====================================
    df = df.fillna(0)

    # =====================================
    # FEATURES
    # =====================================
    features = [

        "Open",
        "High",
        "Low",
        "Close",
        "Volume",

        "SMA_5",

        "RSI",

        "MACD",

        "Signal_Line",

        "BB_Middle",
        "BB_Upper",
        "BB_Lower"
    ]

    data = df[features]

    # =====================================
    # SCALE DATA
    # =====================================
    scaled_data = scaler.transform(data)

    # =====================================
    # LAST 60 DAYS
    # =====================================
    last_60_days = scaled_data[-60:]

    X_test = np.array([last_60_days])

    # =====================================
    # PREDICT
    # =====================================
    predicted_price = model.predict(X_test)

    # =====================================
    # INVERSE SCALE
    # =====================================
    dummy_array = np.zeros((1, len(features)))

    dummy_array[0][3] = predicted_price[0][0]

    predicted_price_real = scaler.inverse_transform(
        dummy_array
    )[0][3]

    # =====================================
    # CURRENT PRICE
    # =====================================
    current_price = df["Close"].iloc[-1]

    # =====================================
    # TREND
    # =====================================
    if predicted_price_real > current_price:

        trend = "BULLISH"

    else:

        trend = "BEARISH"

    # =====================================
    # RETURN
    # =====================================
    return {

        "stock": symbol,

        "current_price": round(float(current_price), 2),

        "predicted_price": round(float(predicted_price_real), 2),

        "trend": trend
    }

# =====================================
# INTRADAY AI PREDICTION API
# =====================================

@app.get("/intraday_predict/{model}/{stock}")
def intraday_predict(
    model: str,
    stock: str
):

    from datetime import (
        datetime,
        timedelta
    )

    # =================================
    # FORMAT SYMBOL
    # =================================
    symbol = stock.upper()

    if (
        ".NS" not in symbol
        and ".BO" not in symbol
    ):
        symbol += ".NS"

    # =================================
    # DOWNLOAD DATA
    # =================================
    df = yf.download(

        symbol,

        period="5d",

        interval="5m",

        auto_adjust=False
    )

    # =================================
    # EMPTY CHECK
    # =================================
    if df.empty:

        return {
            "error": "No data found"
        }

    # =================================
    # FIX MULTI INDEX
    # =================================
    if isinstance(df.columns, pd.MultiIndex):

        df.columns = (
            df.columns
            .get_level_values(0)
        )

    # =================================
    # RESET INDEX
    # =================================
    df.reset_index(inplace=True)

    # =================================
    # CURRENT PRICE
    # =================================
    current_price = round(

        float(df["Close"].iloc[-1]),

        2
    )

    # =================================
    # CURRENT TIME
    # =================================
    current_time = datetime.now()

    # =================================
    # SMA
    # =================================
    df["SMA_5"] = (

        df["Close"]
        .rolling(window=5)
        .mean()
    )

    # =================================
    # RSI
    # =================================
    delta = df["Close"].diff()

    gain = delta.where(delta > 0, 0)

    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(14).mean()

    avg_loss = loss.rolling(14).mean()

    rs = avg_gain / avg_loss

    df["RSI"] = (
        100 - (100 / (1 + rs))
    )

    # =================================
    # MACD
    # =================================
    short_ema = (
        df["Close"]
        .ewm(span=12, adjust=False)
        .mean()
    )

    long_ema = (
        df["Close"]
        .ewm(span=26, adjust=False)
        .mean()
    )

    df["MACD"] = (
        short_ema - long_ema
    )

    df["Signal_Line"] = (
        df["MACD"]
        .ewm(span=9, adjust=False)
        .mean()
    )

    # EMA 20
    df["EMA_20"] = (
        df["Close"]
        .ewm(span=20, adjust=False)
        .mean()
    )

    # EMA 50
    df["EMA_50"] = (
        df["Close"]
        .ewm(span=50, adjust=False)
        .mean()
    )

    # Volatility
    df["Volatility"] = (
        df["Close"]
        .rolling(10)
        .std()
    )

    # Momentum
    df["Momentum"] = (
        df["Close"]
        - df["Close"].shift(10)
    )

    # VWAP
    df["VWAP"] = (
        (df["Close"] * df["Volume"]).cumsum()
        /
        df["Volume"].cumsum()
    )

    # =================================
    # HANDLE NaN
    # =================================
    df = df.fillna(0)

    # =================================
    # FEATURES
    # =================================
    features = [

    "Open",
    "High",
    "Low",
    "Close",
    "Volume",

    "SMA_5",

    "EMA_20",

    "EMA_50",

    "RSI",

    "MACD",

    "Signal_Line",

    "Volatility",

    "Momentum",

    "VWAP"
]

    # =================================
    # SCALE
    # =================================
    data = df[features]

    scaled_data = intraday_scaler.transform(
        data
    )

    # =================================
    # LAST 60
    # =================================
    last_60 = scaled_data[-60:]

    X_test = last_60.reshape(
        1,
        -1
    )

    # =================================
    # MODEL SELECTION
    # =================================

    if model == "xgboost":

        predictions = (
            intraday_model.predict(
                X_test
            )[0]
        )

    elif model == "catboost":

        predictions = (
            catboost_model.predict(
                X_test
            )[0]
        )

    else:

        return {
            "error":
            "Invalid model selected"
        }

    # =================================
    # CONVERT BACK TO REAL PRICE
    # =================================
    future_prices = []

    running_price = current_price

    for change in predictions:

        running_price = running_price * (
            1 + change
        )

        future_prices.append(
            round(
                float(running_price),
                2
            )
         )

    # =================================
    # MARKET CLOSE TIME
    # =================================
    market_close = current_time.replace(

        hour=15,

        minute=30,

        second=0,

        microsecond=0
    )

    # =================================
    # REMAINING CANDLES
    # =================================
    remaining_minutes = int(

        (
            market_close - current_time
        ).total_seconds() / 60
    )

    remaining_steps = max(

        1,

        remaining_minutes // 5
    )

    # =================================
    # LIMIT PREDICTIONS
    # =================================
    future_prices = future_prices[
        :remaining_steps
    ]

    # =================================
    # TIME GENERATION
    # =================================
    future_times = []

    future_now = current_time

    for i in range(
        remaining_steps
    ):

        future_now += timedelta(
            minutes=5
        )

        future_times.append(

            future_now.strftime(
                "%I:%M %p"
            )
        )

    # =================================
    # SESSION FORECAST
    # =================================
    session_forecast = []

    for i in range(
        len(future_prices)
    ):

        session_forecast.append({

            "time":
                future_times[i],

            "price":
                future_prices[i]
        })

    # =================================
    # TREND
    # =================================
    if future_prices[-1] > current_price:

        trend = "BULLISH"

    else:

        trend = "BEARISH"

    # =================================
    # CONFIDENCE
    # =================================
    movement = abs(

        (
            future_prices[-1]
            - current_price
        )

        / current_price
    )

    if movement < 0.01:

        confidence = "82%"

    elif movement < 0.03:

        confidence = "74%"

    else:

        confidence = "66%"

    # =================================
    # RESPONSE
    # =================================
    return {

        "current_price":
            current_price,

        "current_time":
            current_time.strftime(
                "%d-%m-%Y %I:%M %p"
            ),

        "trend":
            trend,

        "confidence":
            confidence,

        "market_close_prediction":
            future_prices[-1],

        "session_forecast":
            session_forecast
    }
# =====================================
# LIVE NIFTY TICKER
# =====================================
@app.get("/ticker")
def live_ticker():

    stocks = [

        "RELIANCE.NS",

        "INFY.NS",

        "TCS.NS",

        "SBIN.NS",

        "HDFCBANK.NS",

        "ITC.NS"
    ]

    result = []

    for stock in stocks:

        try:

            ticker = yf.Ticker(stock)

            info = ticker.info

            result.append({

                "symbol":
                    stock.replace(".NS", ""),

                "price":
                    round(
                        info.get(
                            "currentPrice",
                            0
                        ),
                        2
                    ),

                "change":
                    round(
                        info.get(
                            "regularMarketChangePercent",
                            0
                        ),
                        2
                    )
            })

        except Exception:

            continue

    return result

# =====================================
# MARKET OVERVIEW
# =====================================
@app.get("/market_overview")
def market_overview():

    stocks = [

        "RELIANCE.NS",

        "INFY.NS",

        "TCS.NS",

        "SBIN.NS",

        "HDFCBANK.NS",

        "ITC.NS",

        "LT.NS",

        "ICICIBANK.NS"
    ]

    market_data = []

    for stock in stocks:

        try:

            ticker = yf.Ticker(stock)

            info = ticker.info

            symbol = stock.replace(
                ".NS",
                ""
            )

            price = round(
                info.get(
                    "currentPrice",
                    0
                ),
                2
            )

            change = round(
                info.get(
                    "regularMarketChangePercent",
                    0
                ),
                2
            )

            market_data.append({

                "symbol": symbol,

                "price": price,

                "change": change
            })

        except Exception:

            continue

    # =====================================
    # SORTING
    # =====================================
    gainers = sorted(

        market_data,

        key=lambda x: x["change"],

        reverse=True
    )

    losers = sorted(

        market_data,

        key=lambda x: x["change"]
    )

    market_trend = "BULLISH"

    avg_change = sum(
        item["change"]
        for item in market_data
    ) / len(market_data)

    if avg_change < 0:

        market_trend = "BEARISH"

    return {

        "trend": market_trend,

        "top_gainer": gainers[0],

        "top_loser": losers[0],

        "stocks": market_data
    }


@app.get("/nifty_live")
def nifty_live():

    df = yf.download(
        "^NSEI",
        period="1d",
        interval="5m",
        auto_adjust=False,
        progress=False
    )

    if df.empty:
        return {"error": "No data"}

    chart_data = []

    for index, row in df.iterrows():

        chart_data.append({

            "time": index.strftime("%H:%M"),

            "price": round(
                float(row["Close"]),
                2
            )
        })

    current_price = float(
        df["Close"].iloc[-1]
    )

    high_price = float(
        df["High"].max()
    )

    low_price = float(
        df["Low"].min()
    )

    open_price = float(
        df["Open"].iloc[0]
    )

    change_percent = round(

        (
            (current_price - open_price)
            / open_price
        ) * 100,

        2
    )

    return {

        "current": round(current_price, 2),

        "high": round(high_price, 2),

        "low": round(low_price, 2),

        "change": change_percent,

        "chart_data": chart_data
    }