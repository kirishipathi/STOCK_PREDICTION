import yfinance as yf
import pandas as pd

# =====================================
# STOCK LIST
# =====================================
stocks = [

    "ADANIENT.NS",
    "ADANIPORTS.NS",
    "APOLLOHOSP.NS",
    "ASIANPAINT.NS",
    "AXISBANK.NS",
    "BAJAJ-AUTO.NS",
    "BAJFINANCE.NS",
    "BAJAJFINSV.NS",
    "BEL.NS",
    "BHARTIARTL.NS",
    "BPCL.NS",
    "BRITANNIA.NS",
    "CIPLA.NS",
    "COALINDIA.NS",
    "DRREDDY.NS",
    "EICHERMOT.NS",
    "ETERNAL.NS",
    "GRASIM.NS",
    "HCLTECH.NS",
    "HDFCBANK.NS",
    "HDFCLIFE.NS",
    "HEROMOTOCO.NS",
    "HINDALCO.NS",
    "HINDUNILVR.NS",
    "ICICIBANK.NS",
    "INDUSINDBK.NS",
    "INFY.NS",
    "ITC.NS",
    "JIOFIN.NS",
    "JSWSTEEL.NS",
    "KOTAKBANK.NS",
    "LT.NS",
    "M&M.NS",
    "MARUTI.NS",
    "NESTLEIND.NS",
    "NTPC.NS",
    "ONGC.NS",
    "POWERGRID.NS",
    "RELIANCE.NS",
    "SBILIFE.NS",
    "SBIN.NS",
    "SHRIRAMFIN.NS",
    "SUNPHARMA.NS",
    "TATACONSUM.NS",
    "TATAMOTORS.NS",
    "TATASTEEL.NS",
    "TCS.NS",
    "TECHM.NS",
    "TITAN.NS",
    "ULTRACEMCO.NS",
    "WIPRO.NS"
]

# =====================================
# FINAL DATASET
# =====================================
all_data = []

# =====================================
# LOOP THROUGH STOCKS
# =====================================
for stock in stocks:

    print(f"\nDownloading {stock}...")

    try:

        # =====================================
        # DOWNLOAD DATA
        # =====================================
        df = yf.download(
            stock,
            period="5y",
            interval="1d",
            auto_adjust=False
        )

        # =====================================
        # FIX MULTI-INDEX COLUMNS
        # =====================================
        if isinstance(df.columns, pd.MultiIndex):

            df.columns = (
                df.columns
                .get_level_values(0)
            )

        # =====================================
        # EMPTY CHECK
        # =====================================
        if df.empty:

            print(f"No data for {stock}")
            continue

        # =====================================
        # RESET INDEX
        # =====================================
        df.reset_index(inplace=True)

        # =====================================
        # ADD STOCK NAME
        # =====================================
        df["Stock"] = stock

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

        gain = delta.where(
            delta > 0,
            0
        )

        loss = -delta.where(
            delta < 0,
            0
        )

        avg_gain = (
            gain
            .rolling(window=14)
            .mean()
        )

        avg_loss = (
            loss
            .rolling(window=14)
            .mean()
        )

        rs = avg_gain / avg_loss

        df["RSI"] = (
            100 - (100 / (1 + rs))
        )

        # =====================================
        # MACD
        # =====================================
        short_ema = (
            df["Close"]
            .ewm(
                span=12,
                adjust=False
            )
            .mean()
        )

        long_ema = (
            df["Close"]
            .ewm(
                span=26,
                adjust=False
            )
            .mean()
        )

        df["MACD"] = (
            short_ema - long_ema
        )

        df["Signal_Line"] = (
            df["MACD"]
            .ewm(
                span=9,
                adjust=False
            )
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
        # KEEP IMPORTANT COLUMNS ONLY
        # =====================================
        df = df[[
            "Date",
            "Stock",
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
        ]]

        # =====================================
        # APPEND DATA
        # =====================================
        all_data.append(df)

        print(f"{stock} completed.")

    except Exception as e:

        print(f"Error in {stock}: {e}")

# =====================================
# COMBINE ALL STOCKS
# =====================================
final_df = pd.concat(
    all_data,
    ignore_index=True
)

# =====================================
# SAVE CSV
# =====================================
final_df.to_csv(
    "training_data.csv",
    index=False
)

print("\n=====================================")
print("Dataset Created Successfully!")
print("=====================================")

print(final_df.head())

print("\nDataset Shape:")
print(final_df.shape)