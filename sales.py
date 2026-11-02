
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
df = pd.read_csv("over all sales data.csv")

# Convert date column
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# Visualization Style
sns.set_style("whitegrid")

# 1. Sales by Category
plt.figure(figsize=(8,5))
sns.barplot(data=df, x='Category', y='Sales', estimator=sum)
plt.title("Total Sales by Category")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# 2. Profit by Region
plt.figure(figsize=(8,5))
sns.barplot(data=df, x='Region', y='Profit', estimator=sum)
plt.title("Profit by Region")
plt.tight_layout()
plt.show()

# 3. Sales by Gender
plt.figure(figsize=(6,5))
df.groupby('Gender')['Sales'].sum().plot(
    kind='pie', autopct='%1.1f%%'
)
plt.title("Sales Distribution by Gender")
plt.ylabel("")
plt.show()

# 4. Monthly Sales Trend
monthly_sales = df.groupby(
    df['Order_Date'].dt.to_period('M')
)['Sales'].sum()

plt.figure(figsize=(10,5))
monthly_sales.plot(kind='line', marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Top 10 Products by Sales
top_products = df.groupby(
    'Product'
)['Sales'].sum().nlargest(10)

plt.figure(figsize=(9,5))
top_products.sort_values().plot(kind='barh')
plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales")
plt.tight_layout()
plt.show()

# 6. Payment Mode Analysis
plt.figure(figsize=(7,5))
sns.countplot(data=df, x='Payment_Mode')
plt.title("Orders by Payment Mode")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

# 7. Sales vs Profit
plt.figure(figsize=(8,5))
sns.scatterplot(
    data=df, x='Sales', y='Profit',
    hue='Category'
)
plt.title("Sales vs Profit Analysis")
plt.tight_layout()
plt.show()

# 8. Order Status Analysis
plt.figure(figsize=(7,5))
sns.countplot(data=df, x='Order_Status')
plt.title("Order Status Distribution")
plt.tight_layout()
plt.show()

print("All Data Visualizations Completed!")
