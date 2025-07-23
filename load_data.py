import sqlite3
import pandas as pd

# File paths
db_path = "db/ecommerce.db"
csvs = {
    "total_sales_metrics": "Product-Level Total Sales and Metrics.csv",
    "ad_sales_metrics": "Product-Level Ad Sales and Metrics.csv",
    "eligibility": "Product-Level Eligibility Table.csv"
}

# Table schemas
schemas = {
    "total_sales_metrics": """
        CREATE TABLE IF NOT EXISTS total_sales_metrics (
            date TEXT,
            item_id TEXT,
            total_sales REAL,
            total_units_ordered INTEGER
        );
    """,
    "ad_sales_metrics": """
        CREATE TABLE IF NOT EXISTS ad_sales_metrics (
            date TEXT,
            item_id TEXT,
            ad_sales REAL,
            impressions INTEGER,
            ad_spend REAL,
            clicks INTEGER,
            units_sold INTEGER
        );
    """,
    "eligibility": """
        CREATE TABLE IF NOT EXISTS eligibility (
            eligibility_datetime_utc TEXT,
            item_id TEXT,
            eligibility TEXT,
            message TEXT
        );
    """
}

# Connect to DB
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create tables
for table, schema in schemas.items():
    cur.execute(schema)

# Import CSVs
for table, csv_file in csvs.items():
    df = pd.read_csv(csv_file)
    df.to_sql(table, conn, if_exists='replace', index=False)
    print(f"Imported {csv_file} into {table}")

conn.commit()
conn.close()
print("All data imported successfully.")