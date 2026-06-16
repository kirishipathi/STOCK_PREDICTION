import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler

import joblib

# =====================================
# LOAD DATA
# =====================================
print("Loading intraday dataset...")

df = pd.read_csv(
    "intraday_data.csv"
)

print("Dataset Loaded!")

# =====================================
# SORT
# =====================================
df = df.sort_values(
    by=["Stock", "Datetime"]
)

# =====================================
# CREATE FUTURE TARGET
# =====================================
print("Creating targets...")

df["Future_Close"] = (

    df.groupby("Stock")["Close"]
    .shift(-1)
)

# =====================================
# PERCENTAGE MOVEMENT TARGET
# =====================================
df["Target"] = (

    (
        df["Future_Close"]
        - df["Close"]
    )

    / df["Close"]
)

# =====================================
# REMOVE NaN
# =====================================
df = df.dropna()

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

    "EMA_20",

    "EMA_50",

    "RSI",

    "MACD",

    "Signal_Line",

    "Volatility",

    "Momentum",

    "VWAP"
]

# =====================================
# FEATURE DATA
# =====================================
data = df[features]

# =====================================
# SCALE FEATURES
# =====================================
print("Scaling features...")

scaler = MinMaxScaler()

scaled_data = scaler.fit_transform(
    data
)

# =====================================
# SAVE SCALER
# =====================================
joblib.dump(

    scaler,

    "intraday_scaler.save"
)

print("Scaler Saved!")

# =====================================
# TARGET
# =====================================
target = df["Target"].values

# =====================================
# CREATE SEQUENCES
# =====================================
X = []

y = []

sequence_length = 60

future_steps = 72

print("Creating sequences...")

# =====================================
# MULTI STEP SEQUENCES
# =====================================
for i in range(

    sequence_length,

    len(scaled_data) - future_steps
):

    # =========================
    # INPUT SEQUENCE
    # =========================
    X.append(

        scaled_data[
            i-sequence_length:i
        ]
    )

    # =========================
    # FUTURE TARGETS
    # =========================
    y.append(

        target[
            i:i+future_steps
        ]
    )

# =====================================
# NUMPY
# =====================================
X = np.array(X)

y = np.array(y)

# =====================================
# SAVE
# =====================================
np.save(
    "X_intraday.npy",
    X
)

np.save(
    "y_intraday.npy",
    y
)

# =====================================
# INFO
# =====================================
print("\n=================================")
print("ADVANCED DATA PREP COMPLETE")
print("=================================")

print("\nX shape:", X.shape)

print("y shape:", y.shape)

print("\nForecast Horizon:")

print("72 future candles")

print("\nTarget Type:")

print("Percentage Movement Prediction")

print("\nSaved Files:")

print("X_intraday.npy")
print("y_intraday.npy")
print("intraday_scaler.save")