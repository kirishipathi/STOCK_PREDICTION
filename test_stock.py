import yfinance as yf

stock = yf.Ticker("RELIANCE.NS")

data = stock.history(start="2026-05-01", end="2026-05-31")

print(data)