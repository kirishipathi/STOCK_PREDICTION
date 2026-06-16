import numpy as np

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import (

    LSTM,

    Dense,

    Dropout,

    Bidirectional
)

from tensorflow.keras.callbacks import (

    EarlyStopping,

    ReduceLROnPlateau
)

# =====================================
# LOAD DATA
# =====================================
print("Loading training data...")

X = np.load(
    "X_intraday.npy"
)

y = np.load(
    "y_intraday.npy"
)

print("\nData Loaded!")

print("X shape:", X.shape)

print("y shape:", y.shape)

# =====================================
# BUILD MODEL
# =====================================
print("\nBuilding advanced LSTM model...")

model = Sequential()

# =====================================
# FIRST BiLSTM
# =====================================
model.add(

    Bidirectional(

        LSTM(

            128,

            return_sequences=True
        ),

        input_shape=(
            X.shape[1],
            X.shape[2]
        )
    )
)

model.add(
    Dropout(0.3)
)

# =====================================
# SECOND BiLSTM
# =====================================
model.add(

    Bidirectional(

        LSTM(

            128,

            return_sequences=False
        )
    )
)

model.add(
    Dropout(0.3)
)

# =====================================
# DENSE
# =====================================
model.add(
    Dense(128, activation="relu")
)

model.add(
    Dropout(0.2)
)

# =====================================
# OUTPUT
# =====================================
model.add(
    Dense(72)
)

# =====================================
# COMPILE
# =====================================
model.compile(

    optimizer="adam",

    loss="huber"
)

# =====================================
# SUMMARY
# =====================================
print("\nModel Summary:\n")

model.summary()

# =====================================
# CALLBACKS
# =====================================
early_stop = EarlyStopping(

    monitor="val_loss",

    patience=10,

    restore_best_weights=True
)

reduce_lr = ReduceLROnPlateau(

    monitor="val_loss",

    factor=0.5,

    patience=5,

    verbose=1
)

# =====================================
# TRAIN
# =====================================
print("\nTraining advanced model...\n")

history = model.fit(

    X,

    y,

    epochs=100,

    batch_size=128,

    validation_split=0.2,

    callbacks=[

        early_stop,

        reduce_lr
    ]
)

# =====================================
# SAVE MODEL
# =====================================
model.save(
    "intraday_lstm_model.h5"
)

# =====================================
# DONE
# =====================================
print("\n=================================")
print("ADVANCED MODEL TRAINING COMPLETE")
print("=================================")

print("\nModel saved as:")

print("intraday_lstm_model.h5")