import sqlite3
import yfinance as yf
import pandas as pd

conn = sqlite3.connect("stocks.db")

stocks = ["RELIANCE", "TCS", "INFY"]

all_data = []

for stock_name in stocks:
    try:
        print(f"Fetching {stock_name}...")

        stock = yf.Ticker(stock_name + ".NS")
        data = stock.history(period="3mo")

        if data.empty:
            print(f"⚠️ No data for {stock_name}, skipping...")
            continue

        data.reset_index(inplace=True)
        data["Stock"] = stock_name

        all_data.append(data)

    except Exception as e:
        print(f"❌ Error fetching {stock_name}: {e}")

# only combine if data exists
if all_data:
    final_df = pd.concat(all_data)
    final_df.to_sql("stocks", conn, if_exists="replace", index=False)
    print("✅ Data saved successfully!")
else:
    print("❌ No data fetched at all!")