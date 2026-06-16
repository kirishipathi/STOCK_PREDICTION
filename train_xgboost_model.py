import numpy as np
import joblib
import time

from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split

from xgboost import XGBRegressor

# =====================================
# LOAD DATA
# =====================================
print("Loading prepared data...")

X = np.load("X_intraday.npy")
y = np.load("y_intraday.npy")

print("\nOriginal Shapes:")

print("X:", X.shape)

print("y:", y.shape)

# =====================================
# FLATTEN DATA
# =====================================
print("\nFlattening sequences...")

samples = X.shape[0]

X = X.reshape(samples, -1)

print("Flattened X Shape:", X.shape)

# =====================================
# TRAIN TEST SPLIT
# =====================================
print("\nSplitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    shuffle=False
)

print("Train Shape:", X_train.shape)

print("Test Shape :", X_test.shape)

# =====================================
# BUILD MODEL
# =====================================
print("\nBuilding XGBoost model...")

base_model = XGBRegressor(

    n_estimators=200,

    max_depth=6,

    learning_rate=0.05,

    subsample=0.8,

    colsample_bytree=0.8,

    objective="reg:squarederror",

    random_state=42,

    n_jobs=-1,

    tree_method="hist"
)

model = MultiOutputRegressor(
    base_model
)

# =====================================
# TRAIN
# =====================================
print("\nTraining XGBoost...\n")

start_time = time.time()

model.fit(

    X_train,

    y_train
)

end_time = time.time()

training_minutes = (

    end_time - start_time
) / 60

print("\nTraining Complete!")

# =====================================
# EVALUATE
# =====================================
print("\nEvaluating Model...")

preds = model.predict(
    X_test
)

mae = np.mean(

    np.abs(
        preds - y_test
    )
)

print(f"\nMAE: {mae:.10f}")

print(
    f"\nTraining Time: "
    f"{training_minutes:.2f} minutes"
)

# =====================================
# SAVE MODEL
# =====================================
print("\nSaving model...")

joblib.dump(

    model,

    "xgboost_intraday_model.pkl"
)

print("\n=================================")
print("XGBOOST MODEL TRAINING COMPLETE")
print("=================================")

print("\nSaved Files:")

print("xgboost_intraday_model.pkl")