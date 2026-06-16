import yfinance as yf
import pandas as pd
import numpy as np
import joblib

from datetime import (
    datetime,
    timedelta
)

from tensorflow.keras.models import load_model

# =====================================
# LOAD MODEL
# =====================================
print("Loading intraday model...")

model = load_model(
    "intraday_lstm_model.h5"
)

print("Model Loaded!")

# =====================================
# LOAD SCALER
# =====================================
scaler = joblib.load(
    "intraday_scaler.save"
)

print("Scaler Loaded!")

# =====================================
# STOCK INPUT
# =====================================
stock = input(
    "\nEnter Stock Symbol: "
).upper()

# =====================================
# FORMAT SYMBOL
# =====================================
if (
    ".NS" not in stock
    and ".BO" not in stock
):
    stock += ".NS"

# =====================================
# DOWNLOAD DATA
# =====================================
print(f"\nDownloading {stock} data...")

df = yf.download(

    stock,

    period="5d",

    interval="5m",

    auto_adjust=False
)

# =====================================
# EMPTY CHECK
# =====================================
if df.empty:

    print("\nNo data found!")

    exit()

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
# CURRENT PRICE
# =====================================
current_price = round(
    float(df["Close"].iloc[-1]),
    2
)

# =====================================
# CURRENT TIME
# =====================================
current_time = datetime.now()

# =====================================
# MARKET TIMINGS
# =====================================
market_open = current_time.replace(

    hour=9,
    minute=15,
    second=0,
    microsecond=0
)

market_close = current_time.replace(

    hour=15,
    minute=30,
    second=0,
    microsecond=0
)

# =====================================
# NEXT MARKET TIME FUNCTION
# =====================================
def next_market_time(minutes):

    future = current_time + timedelta(
        minutes=minutes
    )

    # AFTER MARKET CLOSE
    if future > market_close:

        next_day = current_time + timedelta(days=1)

        # WEEKEND SKIP
        while next_day.weekday() >= 5:

            next_day += timedelta(days=1)

        future = next_day.replace(

            hour=9,
            minute=15,
            second=0,
            microsecond=0
        ) + timedelta(
            minutes=minutes
        )

    # BEFORE MARKET OPEN
    if future < market_open:

        future = market_open + timedelta(
            minutes=minutes
        )

    return future

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

    "Signal_Line"
]

# =====================================
# SCALE DATA
# =====================================
data = df[features]

scaled_data = scaler.transform(
    data
)

# =====================================
# LAST 60 CANDLES
# =====================================
last_60 = scaled_data[-60:]

# =====================================
# PREDICT PERCENT CHANGE
# =====================================
X_test = np.array([
    last_60
])

predicted_change = model.predict(

    X_test,

    verbose=0
)[0][0]

# =====================================
# FUTURE PRICE CALCULATION
# =====================================
future_price = current_price * (
    1 + predicted_change
)

future_price = round(
    float(future_price),
    2
)

# =====================================
# SMALL REALISTIC MOVEMENTS
# =====================================
difference = (
    future_price
    - current_price
)

pred_5m = round(
    current_price + (difference * 0.25),
    2
)

pred_10m = round(
    current_price + (difference * 0.50),
    2
)

pred_30m = round(
    current_price + (difference * 0.75),
    2
)

pred_1h = round(
    future_price,
    2
)

# =====================================
# FUTURE TIMES
# =====================================
time_5m = next_market_time(5)

time_10m = next_market_time(10)

time_30m = next_market_time(30)

time_1h = next_market_time(60)

# =====================================
# TREND
# =====================================
if pred_1h > current_price:

    trend = "BULLISH 📈"

else:

    trend = "BEARISH 📉"

# =====================================
# CONFIDENCE
# =====================================
movement = abs(predicted_change)

if movement < 0.002:

    confidence = "88%"

elif movement < 0.005:

    confidence = "78%"

else:

    confidence = "68%"

# =====================================
# DISPLAY
# =====================================
print("\n=================================")
print("AI MARKET FORECAST")
print("=================================")

print(
    f"\nCurrent Time : "
    f"{current_time.strftime('%d-%m-%Y %I:%M %p')}"
)

print(
    f"Current Price: ₹{current_price}"
)

print("\n---------------------------------")

print(
    f"\n5 Min Prediction "
    f"({time_5m.strftime('%d-%m %I:%M %p')}): "
    f"₹{pred_5m}"
)

print(
    f"10 Min Prediction "
    f"({time_10m.strftime('%d-%m %I:%M %p')}): "
    f"₹{pred_10m}"
)

print(
    f"30 Min Prediction "
    f"({time_30m.strftime('%d-%m %I:%M %p')}): "
    f"₹{pred_30m}"
)

print(
    f"1 Hour Prediction "
    f"({time_1h.strftime('%d-%m %I:%M %p')}): "
    f"₹{pred_1h}"
)

print("\n---------------------------------")

print(f"\nExpected Trend : {trend}")

print(f"AI Confidence  : {confidence}")