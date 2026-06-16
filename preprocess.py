import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split

import joblib

# =====================================
# LOAD DATASET
# =====================================
print("Loading dataset...")

df = pd.read_csv("training_data.csv")

print(df.head())

# =====================================
# FEATURES FOR ML
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

# =====================================
# KEEP ONLY FEATURES
# =====================================
data = df[features]

# =====================================
# SCALE DATA
# =====================================
print("\nScaling data...")

scaler = MinMaxScaler()

scaled_data = scaler.fit_transform(data)

# Save scaler
joblib.dump(
    scaler,
    "scaler.save"
)

print("Scaler saved.")

# =====================================
# CREATE SEQUENCES
# =====================================
sequence_length = 60

X = []
y = []

print("\nCreating sequences...")

for i in range(
    sequence_length,
    len(scaled_data)
):

    # Past 60 days
    X.append(
        scaled_data[
            i-sequence_length:i
        ]
    )

    # Predict CLOSE price
    y.append(
        scaled_data[i][3]
    )

# Convert to numpy
X = np.array(X)

y = np.array(y)

print("\nSequence creation completed.")

# =====================================
# TRAIN TEST SPLIT
# =====================================
X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    shuffle=False
)

# =====================================
# SAVE PREPROCESSED FILES
# =====================================
np.save("X_train.npy", X_train)

np.save("X_test.npy", X_test)

np.save("y_train.npy", y_train)

np.save("y_test.npy", y_test)

print("\n====================================")
print("PREPROCESSING COMPLETED")
print("====================================")

print(f"\nX_train shape: {X_train.shape}")

print(f"y_train shape: {y_train.shape}")

print(f"\nX_test shape: {X_test.shape}")

print(f"y_test shape: {y_test.shape}")