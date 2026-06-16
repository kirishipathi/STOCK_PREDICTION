import numpy as np

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import (
    LSTM,
    Dense,
    Dropout
)

from tensorflow.keras.callbacks import EarlyStopping

import matplotlib.pyplot as plt

# =====================================
# LOAD PREPROCESSED DATA
# =====================================
print("Loading training data...")

X_train = np.load("X_train.npy")

X_test = np.load("X_test.npy")

y_train = np.load("y_train.npy")

y_test = np.load("y_test.npy")

print("\nData Loaded Successfully!")

print(f"\nX_train shape: {X_train.shape}")

print(f"y_train shape: {y_train.shape}")

# =====================================
# BUILD LSTM MODEL
# =====================================
print("\nBuilding LSTM model...")

model = Sequential()

# =====================================
# FIRST LSTM LAYER
# =====================================
model.add(

    LSTM(

        units=64,

        return_sequences=True,

        input_shape=(
            X_train.shape[1],
            X_train.shape[2]
        )
    )
)

model.add(
    Dropout(0.2)
)

# =====================================
# SECOND LSTM LAYER
# =====================================
model.add(

    LSTM(
        units=64
    )
)

model.add(
    Dropout(0.2)
)

# =====================================
# OUTPUT LAYER
# =====================================
model.add(
    Dense(1)
)

# =====================================
# COMPILE MODEL
# =====================================
model.compile(

    optimizer="adam",

    loss="mean_squared_error"
)

print("\nModel Summary:\n")

model.summary()

# =====================================
# EARLY STOPPING
# =====================================
early_stop = EarlyStopping(

    monitor="val_loss",

    patience=5,

    restore_best_weights=True
)

# =====================================
# TRAIN MODEL
# =====================================
print("\nTraining model...\n")

history = model.fit(

    X_train,

    y_train,

    validation_data=(
        X_test,
        y_test
    ),

    epochs=25,

    batch_size=32,

    callbacks=[early_stop]
)

# =====================================
# SAVE MODEL
# =====================================
model.save(
    "stock_lstm_model.h5"
)

print("\n====================================")
print("MODEL TRAINING COMPLETED")
print("====================================")

print("\nModel saved as:")
print("stock_lstm_model.h5")

# =====================================
# PLOT LOSS GRAPH
# =====================================
plt.figure(figsize=(10, 5))

plt.plot(
    history.history["loss"],
    label="Training Loss"
)

plt.plot(
    history.history["val_loss"],
    label="Validation Loss"
)

plt.title("LSTM Training Loss")

plt.xlabel("Epoch")

plt.ylabel("Loss")

plt.legend()

plt.grid(True)

plt.show()