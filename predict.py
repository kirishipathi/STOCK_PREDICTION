import yfinance as yf
import pandas as pd
import numpy as np
import joblib

from tensorflow.keras.models import load_model

import matplotlib.pyplot as plt

# =====================================
# LOAD TRAINED MODEL
# =====================================
print("Loading trained model...")

model = load_model("stock_lstm_model.h5")

print("Model loaded.")

# =====================================
# LOAD SCALER
# =====================================
scaler = joblib.load("scaler.save")

print("Scaler loaded.")

# =====================================
# STOCK INPUT
# =====================================
stock = input("Enter Stock Symbol: ")

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
    period="1y",
    interval="1d",
    auto_adjust=False
)

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
# EMPTY DATA CHECK
# =====================================
if df.empty:

    print("\nInvalid or unavailable stock symbol.")

    exit()

# =====================================
# INDICATORS
# =====================================

# SMA
df["SMA_5"] = (
    df["Close"]
    .rolling(window=5)
    .mean()
)

# RSI
delta = df["Close"].diff()

gain = delta.where(delta > 0, 0)

loss = -delta.where(delta < 0, 0)

avg_gain = gain.rolling(14).mean()

avg_loss = loss.rolling(14).mean()

rs = avg_gain / avg_loss

df["RSI"] = (
    100 - (100 / (1 + rs))
)

# MACD
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

# Bollinger Bands
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
print("\nPredicting future price...")

predicted_price = model.predict(X_test)

# =====================================
# INVERSE TRANSFORM
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
# RESULTS
# =====================================
print("\n====================================")
print("PREDICTION RESULT")
print("====================================")

print(f"\nCurrent Price: ₹{current_price:.2f}")

print(f"Predicted Next Price: ₹{predicted_price_real:.2f}")

# =====================================
# FUTURE TREND
# =====================================
if predicted_price_real > current_price:

    print("\nPrediction: 📈 BULLISH")

else:

    print("\nPrediction: 📉 BEARISH")

# =====================================
# GRAPH
# =====================================
plt.figure(figsize=(12, 6))

plt.plot(

    df["Date"].tail(60),

    df["Close"].tail(60),

    label="Historical Prices"
)

plt.scatter(

    df["Date"].iloc[-1],

    predicted_price_real,

    color="red",

    s=100,

    label="Predicted Next Price"
)

plt.title(f"{stock} Future Prediction")

plt.xlabel("Date")

plt.ylabel("Price")

plt.legend()

plt.grid(True)

plt.show()