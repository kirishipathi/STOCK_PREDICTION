import yfinance as yf
import pandas as pd

# =====================================
# STOCK LIST
# =====================================
stocks = [

    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "ITC.NS",
    "LT.NS",
    "KOTAKBANK.NS",
    "AXISBANK.NS",

    "ASIANPAINT.NS",
    "BAJFINANCE.NS",
    "BAJAJFINSV.NS",
    "BHARTIARTL.NS",
    "BPCL.NS",
    "BRITANNIA.NS",
    "CIPLA.NS",
    "COALINDIA.NS",
    "DIVISLAB.NS",
    "DRREDDY.NS",

    "EICHERMOT.NS",
    "GRASIM.NS",
    "HCLTECH.NS",
    "HINDALCO.NS",
    "HINDUNILVR.NS",
    "INDUSINDBK.NS",
    "JSWSTEEL.NS",
    "MARUTI.NS",
    "NESTLEIND.NS",
    "NTPC.NS",

    "ONGC.NS",
    "POWERGRID.NS",
    "SBILIFE.NS",
    "SHRIRAMFIN.NS",
    "SUNPHARMA.NS",
    "TATACONSUM.NS",
    "TATASTEEL.NS",
    "TECHM.NS",
    "TITAN.NS",

    "ULTRACEMCO.NS",
    "UPL.NS",
    "WIPRO.NS",
    "ADANIENT.NS",
    "ADANIPORTS.NS",
    "APOLLOHOSP.NS",
    "HEROMOTOCO.NS",
    "M&M.NS",
    "PIDILITIND.NS",
    "SIEMENS.NS"
]

# =====================================
# FINAL STORAGE
# =====================================
all_data = []

# =====================================
# LOOP STOCKS
# =====================================
for stock in stocks:

    print("\n=================================")

    print(f"DOWNLOADING: {stock}")

    print("=================================")

    try:

        # =================================
        # DOWNLOAD 55 DAYS OF 5M DATA
        # =================================
        df = yf.download(

            stock,

            period="55d",

            interval="5m",

            auto_adjust=False,

            progress=False
        )

        # =================================
        # EMPTY CHECK
        # =================================
        if df.empty:

            print(f"No data for {stock}")

            continue

        # =================================
        # FIX MULTI INDEX
        # =================================
        if isinstance(
            df.columns,
            pd.MultiIndex
        ):

            df.columns = (

                df.columns
                .get_level_values(0)
            )

        # =================================
        # RESET INDEX
        # =================================
        df.reset_index(
            inplace=True
        )

        # =================================
        # STOCK NAME
        # =================================
        df["Stock"] = stock

        # =================================
        # SORT
        # =================================
        df.sort_values(

            by="Datetime",

            inplace=True
        )

        # =================================
        # SMA
        # =================================
        df["SMA_5"] = (

            df["Close"]
            .rolling(window=5)
            .mean()
        )

        # =================================
        # EMA 20
        # =================================
        df["EMA_20"] = (

            df["Close"]
            .ewm(span=20, adjust=False)
            .mean()
        )

        # =================================
        # EMA 50
        # =================================
        df["EMA_50"] = (

            df["Close"]
            .ewm(span=50, adjust=False)
            .mean()
        )

        # =================================
        # RSI
        # =================================
        delta = df["Close"].diff()

        gain = delta.where(
            delta > 0,
            0
        )

        loss = -delta.where(
            delta < 0,
            0
        )

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

        # =================================
        # VOLATILITY
        # =================================
        df["Volatility"] = (

            df["High"]
            - df["Low"]
        )

        # =================================
        # MOMENTUM
        # =================================
        df["Momentum"] = (

            df["Close"]
            - df["Close"].shift(5)
        )

        # =================================
        # VWAP
        # =================================
        typical_price = (

            df["High"]
            + df["Low"]
            + df["Close"]

        ) / 3

        df["VWAP"] = (

            (
                typical_price
                * df["Volume"]
            ).cumsum()

            / df["Volume"].cumsum()
        )

        # =================================
        # HANDLE NaN
        # =================================
        df = df.fillna(0)

        # =================================
        # APPEND
        # =================================
        all_data.append(df)

        print(
            f"Downloaded: "
            f"{len(df)} candles"
        )

    except Exception as e:

        print(
            f"ERROR: {e}"
        )

# =====================================
# FINAL DATASET
# =====================================
final_df = pd.concat(

    all_data,

    ignore_index=True
)

# =====================================
# REMOVE DUPLICATES
# =====================================
final_df.drop_duplicates(

    subset=["Stock", "Datetime"],

    inplace=True
)

# =====================================
# SORT FINAL DATA
# =====================================
final_df.sort_values(

    by=["Stock", "Datetime"],

    inplace=True
)

# =====================================
# RESET INDEX
# =====================================
final_df.reset_index(

    drop=True,

    inplace=True
)

# =====================================
# SAVE CSV
# =====================================
final_df.to_csv(

    "intraday_data.csv",

    index=False
)

# =====================================
# DONE
# =====================================
print("\n=================================")
print("MEGA INTRADAY DATASET CREATED")
print("=================================")

print(
    f"\nTotal Candles: "
    f"{len(final_df)}"
)

print("\nSaved as:")

print("intraday_data.csv")