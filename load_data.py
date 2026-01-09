import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv("ola_rides.csv")

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Create SQLite DB
engine = create_engine("sqlite:///ola_db.sqlite")

# Write to DB
df.to_sql(
    name="rides",
    con=engine,
    if_exists="replace",
    index=False
)

print("✅ Data loaded into SQLite successfully")
