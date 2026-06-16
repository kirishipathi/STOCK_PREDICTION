import pandas as pd
import sqlite3

# =========================
# LOAD CSV
# =========================
df = pd.read_csv(
    "training_data.csv"
)

# =========================
# CONNECT DATABASE
# =========================
conn = sqlite3.connect(
    "stocks.db"
)

# =========================
# REPLACE TABLE
# =========================
df.to_sql(

    "stocks",

    conn,

    if_exists="replace",

    index=False
)

# =========================
# DONE
# =========================
print(
    "Database Updated Successfully!"
)

print(df.head())