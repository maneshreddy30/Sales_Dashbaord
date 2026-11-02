"""
Sales Performance Analysis
Run:
    pip install -r requirements.txt
    python python/sales_analysis.py

Input: data/sales_data_raw.csv
Outputs: data/sales_data_cleaned.csv, reports/ charts and summary
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sales_data_raw.csv"
OUT = ROOT / "reports"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(DATA)
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

# Basic data-quality checks
print("Rows and columns:", df.shape)
print("Missing values by column:\n", df.isna().sum())
print("Exact duplicate rows:", df.duplicated().sum())
print("Duplicate order IDs:", df["Order_ID"].duplicated().sum())

# Standardize text columns and validate numeric fields
text_cols = ["Order_ID", "Customer_Name", "Gender", "City", "State",
             "Region", "Category", "Product", "Payment_Mode", "Order_Status"]
for col in text_cols:
    df[col] = df[col].astype("string").str.strip()

numeric_cols = ["Age", "Quantity", "Unit_Price", "Sales", "Discount", "Profit"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Remove exact duplicate rows only; do not remove legitimate negative-profit rows.
df = df.drop_duplicates()
df = df.dropna(subset=["Order_ID", "Order_Date", "Sales", "Profit"])
df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)
df["Calculated_Gross_Sales"] = df["Quantity"] * df["Unit_Price"]
df["Expected_After_Discount"] = (
    df["Calculated_Gross_Sales"] * (1 - df["Discount"])
).round(2)
df.to_csv(ROOT / "data" / "sales_data_cleaned.csv", index=False)

# Summary metrics: values are recorded in the source dataset.
summary = {
    "Rows analysed": len(df),
    "Unique orders": df["Order_ID"].nunique(),
    "Unique customers": df["Customer_Name"].nunique(),
    "Recorded sales": df["Sales"].sum(),
    "Recorded profit": df["Profit"].sum(),
    "Units sold": df["Quantity"].sum(),
    "Average recorded sales per order": df["Sales"].sum() / df["Order_ID"].nunique(),
    "Negative-profit records": int((df["Profit"] < 0).sum()),
    "Cancelled orders": int((df["Order_Status"].str.lower() == "cancelled").sum()),
    "Returned orders": int((df["Order_Status"].str.lower() == "returned").sum()),
}
pd.Series(summary, name="Value").to_csv(OUT / "kpi_summary.csv", header=True)
print("\nKPI SUMMARY\n", pd.Series(summary))

def save_bar(data, x, y, title, xlabel, ylabel, filename, rotate=0):
    ax = data.plot(kind="bar", x=x, y=y, legend=False, figsize=(10, 5))
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=rotate, ha="right" if rotate else "center")
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=160)
    plt.close()

# 1. Sales by category
category = df.groupby("Category", as_index=False)["Sales"].sum().sort_values("Sales", ascending=False)
save_bar(category, "Category", "Sales", "Recorded Sales by Category", "Category", "Sales (INR)", "sales_by_category.png")

# 2. Profit by region
region = df.groupby("Region", as_index=False)["Profit"].sum().sort_values("Profit", ascending=False)
save_bar(region, "Region", "Profit", "Recorded Profit by Region", "Region", "Profit (INR)", "profit_by_region.png")

# 3. Monthly sales trend
monthly = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum().reset_index()
monthly["Month"] = monthly["Order_Date"].astype(str)
ax = monthly.plot(x="Month", y="Sales", kind="line", marker="o", figsize=(11, 5), legend=False)
ax.set_title("Monthly Recorded Sales Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Sales (INR)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(OUT / "monthly_sales_trend.png", dpi=160)
plt.close()

# 4. Top 10 products by recorded sales
top_products = df.groupby("Product", as_index=False)["Sales"].sum().nlargest(10, "Sales").sort_values("Sales")
save_bar(top_products, "Product", "Sales", "Top 10 Products by Recorded Sales", "Product", "Sales (INR)", "top_10_products.png", rotate=35)

# 5. Order status counts
status = df["Order_Status"].value_counts().rename_axis("Order_Status").reset_index(name="Orders")
save_bar(status, "Order_Status", "Orders", "Orders by Status", "Order Status", "Number of Orders", "orders_by_status.png")

# 6. Sales and profit by category (separate scale is not combined)
cat_finance = df.groupby("Category", as_index=False)[["Sales", "Profit"]].sum()
cat_finance.to_csv(OUT / "category_sales_profit.csv", index=False)
print("\nCategory summary:\n", cat_finance.to_string(index=False))
print("\nAnalysis complete. See the reports folder.")
