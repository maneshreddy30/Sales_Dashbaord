# Sales Performance Analysis & Business Intelligence Dashboard

## Project overview
An end-to-end portfolio project analysing a sample retail sales dataset using **MySQL, Excel, Python (Pandas + Matplotlib), and Power BI**. The goal is to convert order-level data into business insights about sales, profitability, products, regions, customers, payments, and order status.

> **Dataset note:** This is a portfolio/sample dataset supplied for analysis. It should not be represented as confidential data from a real company.

## Business questions
1. What are the total recorded sales, profit, order count, and units sold?
2. Which product categories and products contribute the most recorded sales?
3. Which regions perform best by sales and profit?
4. How do sales change month by month?
5. What share of orders are delivered, returned, or cancelled?
6. Which payment methods are most frequently used?
7. Which transactions have negative profit and need investigation?

## Dataset
- Rows: **500**
- Columns: **17**
- Date range: **2025-01-02 to 2025-12-31**
- Unique orders: **500**
- Unique customers: **182**

Fields: Order_ID, Order_Date, Customer_Name, Gender, Age, City, State, Region, Category, Product, Quantity, Unit_Price, Sales, Discount, Profit, Payment_Mode, Order_Status.

## Initial KPI snapshot
| Metric | Value |
|---|---:|
| Recorded sales | ₹11,103,263.00 |
| Recorded profit | ₹1,074,287.64 |
| Orders | 500 |
| Units sold | 1,552 |
| Average recorded sales per order | ₹22,206.53 |
| Negative-profit records | 87 |
| Returned orders | 87 |
| Cancelled orders | 75 |

**Metric definition:** Sales and profit above are sums of values as supplied in the source CSV. The file does not contain a separate refund/return-value column, so recorded sales must not be described as net revenue. Returned orders should be analysed separately. Negative-profit rows are valid investigation targets and must not be deleted simply because profit is negative.

## Repository structure
```text
Sales_Performance_Analysis_Project/
├── data/
│   └── sales_data_raw.csv
├── sql/
│   └── sales_analysis.sql
├── python/
│   └── sales_analysis.py
├── excel/
│   └── Sales_Analysis_Workbook.xlsx
├── powerbi/
│   └── Sales_Performance_Dashboard.pbix
├── screenshots/
├── reports/                  # created when Python script runs
├── requirements.txt
├── .gitignore
└── README.md
```

## Tools and skills demonstrated
- **SQL / MySQL:** table design, aggregation, GROUP BY, ORDER BY, date functions, filtering, top-N analysis, data-quality checks.
- **Excel:** raw-data review, KPI summary, category/region/month/product analysis, filters, workbook organization.
- **Python:** Pandas cleaning and validation, grouping, KPI calculations, Matplotlib charts, CSV exports.
- **Power BI:** interactive KPI cards, slicers, trend and category/region/product visuals, business reporting.

## How to run the Python analysis
1. Install Python 3.10 or later.
2. Open a terminal in the project root.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run:
   ```bash
   python python/sales_analysis.py
   ```
5. Check `data/sales_data_cleaned.csv` and the generated `reports/` folder.

## How to load the dataset into MySQL
1. Open MySQL Workbench and connect to your local MySQL server.
2. Open and execute `sql/sales_analysis.sql` to create the database and table.
3. Right-click the `sales` table and choose **Table Data Import Wizard**.
4. Select `data/sales_data_raw.csv`, confirm comma delimiter and first-row headers, and map columns to the table.
5. Execute the analysis queries in `sql/sales_analysis.sql`.

## Power BI dashboard build / refresh
The `powerbi/` folder contains the PBIX report supplied with this project. Open it in Power BI Desktop. If Power BI asks for the source file, point it to `data/sales_data_raw.csv` (or the original CSV) and refresh.

Recommended report pages:
- **Sales Overview:** recorded sales, recorded profit, orders, units, average sales per order, monthly trend.
- **Product Analysis:** sales/profit by category, top products, quantity by product.
- **Regional Analysis:** sales and profit by region/state/city.
- **Customer Analysis:** unique customers, customer sales ranking, gender and age distributions.
- **Order & Payment Analysis:** delivered/returned/cancelled orders, payment mode mix.
- **Detailed Analysis:** transaction-level table with slicers.

Recommended slicers: Order Date, Region, Category, Order Status, Payment Mode.

Suggested DAX measures (adjust table/column names if your model differs):
```DAX
Total Sales = SUM(sales[Sales])
Total Profit = SUM(sales[Profit])
Total Orders = DISTINCTCOUNT(sales[Order_ID])
Total Quantity = SUM(sales[Quantity])
Unique Customers = DISTINCTCOUNT(sales[Customer_Name])
Average Sales per Order = DIVIDE([Total Sales], [Total Orders])
Profit Margin = DIVIDE([Total Profit], [Total Sales])
Returned Orders = CALCULATE([Total Orders], sales[Order_Status] = "Returned")
Cancelled Orders = CALCULATE([Total Orders], sales[Order_Status] = "Cancelled")
```

## Data quality observations
- Check missing values and duplicate order IDs before publishing.
- Review zero-sales rows alongside their order status.
- Investigate negative-profit transactions; do not automatically delete them.
- Validate date, discount, quantity, and price data types.
- Reconcile Power BI totals against SQL and Excel totals.

## Business recommendations to explore
- Review negative-profit orders to identify pricing, discount, or cost issues.
- Compare category and regional profitability before allocating inventory or promotions.
- Track return and cancellation rates by product and region.
- Monitor monthly trends to plan inventory and sales campaigns.
- Compare payment methods by order volume and recorded sales.

## Limitations
This dataset has 500 rows and represents a sample portfolio exercise, not a production enterprise database. It does not include cost breakdown, refund amounts, shipping charges, or a separate return quantity. Findings are descriptive, not causal.

## Author
**Your Name** — Aspiring Data Analyst

## License
For learning and portfolio demonstration. Confirm dataset permissions before public redistribution.
