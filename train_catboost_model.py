import numpy as np
import time
import joblib

from catboost import CatBoostRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# =========================
# LOAD DATA
# =========================

print("\nLoading dataset...")

X = np.load("X_intraday.npy")
y = np.load("y_intraday.npy")

print("X Shape:", X.shape)
print("Y Shape:", y.shape)

# =========================
# RESHAPE INPUT
# =========================

samples = X.shape[0]

X = X.reshape(samples, -1)

print("Reshaped X:", X.shape)

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    shuffle=False
)

# =========================
# CATBOOST MODEL
# =========================

print("\nTraining CatBoost Model...\n")

start = time.time()

base_model = CatBoostRegressor(

    iterations=300,
    learning_rate=0.05,
    depth=6,

    loss_function="MAE",

    verbose=50,

    random_seed=42
)

model = MultiOutputRegressor(base_model)

model.fit(X_train, y_train)

end = time.time()

# =========================
# PREDICTION
# =========================

print("\nEvaluating Model...\n")

predictions = model.predict(X_test)

# =========================
# MAE
# =========================

mae = mean_absolute_error(
    y_test,
    predictions
)

print(f"\nMAE: {mae:.6f}")

# =========================
# SAVE MODEL
# =========================

joblib.dump(
    model,
    "catboost_intraday_model.pkl"
)

print("\nModel Saved Successfully")

print(
    f"\nTraining Time: {(end - start)/60:.2f} minutes"
)