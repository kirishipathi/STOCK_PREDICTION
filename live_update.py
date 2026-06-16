import sqlite3
import yfinance as yf
import pandas as pd
import time

stocks = [
    "RELIANCE",
    "TCS",
    "INFY"
]

while True:

    print("Updating stock data...")

    conn = sqlite3.connect("stocks.db")

    all_data = []

    for stock_name in stocks:

        try:

            stock = yf.Ticker(
                stock_name + ".NS"
            )

            data = stock.history(
                period="1mo"
            )

            if data.empty:
                continue

            data.reset_index(inplace=True)

            data["Stock"] = stock_name

            all_data.append(data)

            print(f"Updated {stock_name}")

        except Exception as e:

            print(
                f"Error updating {stock_name}: {e}"
            )

    if all_data:

        final_df = pd.concat(all_data)

        final_df.to_sql(
            "stocks",
            conn,
            if_exists="replace",
            index=False
        )

        print("Database updated!")

    conn.close()

    # Wait 60 seconds
    time.sleep(60)