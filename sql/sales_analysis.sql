-- SALES PERFORMANCE ANALYSIS | MySQL 8+
-- Import sales_data_raw.csv into this table using MySQL Workbench
-- Table > Table Data Import Wizard, or LOAD DATA LOCAL INFILE after enabling it.

CREATE DATABASE IF NOT EXISTS sales_analytics;
USE sales_analytics;

DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    Order_ID       VARCHAR(20) PRIMARY KEY,
    Order_Date     DATE,
    Customer_Name  VARCHAR(100),
    Gender         VARCHAR(20),
    Age            INT,
    City           VARCHAR(80),
    State          VARCHAR(80),
    Region         VARCHAR(30),
    Category       VARCHAR(60),
    Product        VARCHAR(100),
    Quantity       INT,
    Unit_Price     DECIMAL(12,2),
    Sales          DECIMAL(14,2),
    Discount       DECIMAL(5,2),
    Profit         DECIMAL(14,2),
    Payment_Mode   VARCHAR(40),
    Order_Status   VARCHAR(30)
);

-- 1. Preview records
SELECT * FROM sales LIMIT 10;

-- 2. Overall KPIs
SELECT
    COUNT(DISTINCT Order_ID) AS total_orders,
    SUM(Quantity) AS total_quantity,
    ROUND(SUM(Sales), 2) AS recorded_sales,
    ROUND(SUM(Profit), 2) AS recorded_profit,
    ROUND(AVG(Sales), 2) AS average_sales_per_order
FROM sales;

-- 3. Sales and profit by category
SELECT Category, ROUND(SUM(Sales),2) AS total_sales,
       ROUND(SUM(Profit),2) AS total_profit
FROM sales
GROUP BY Category
ORDER BY total_sales DESC;

-- 4. Regional performance
SELECT Region, COUNT(*) AS order_count,
       ROUND(SUM(Sales),2) AS total_sales,
       ROUND(SUM(Profit),2) AS total_profit
FROM sales
GROUP BY Region
ORDER BY total_sales DESC;

-- 5. Monthly sales trend
SELECT DATE_FORMAT(Order_Date, '%Y-%m') AS sales_month,
       ROUND(SUM(Sales),2) AS monthly_sales
FROM sales
GROUP BY DATE_FORMAT(Order_Date, '%Y-%m')
ORDER BY sales_month;

-- 6. Top 10 products
SELECT Product, SUM(Quantity) AS units_sold,
       ROUND(SUM(Sales),2) AS total_sales,
       ROUND(SUM(Profit),2) AS total_profit
FROM sales
GROUP BY Product
ORDER BY total_sales DESC
LIMIT 10;

-- 7. Order status distribution
SELECT Order_Status, COUNT(*) AS order_count,
       ROUND(SUM(Sales),2) AS recorded_sales
FROM sales
GROUP BY Order_Status
ORDER BY order_count DESC;

-- 8. Payment mode analysis
SELECT Payment_Mode, COUNT(*) AS orders,
       ROUND(SUM(Sales),2) AS recorded_sales
FROM sales
GROUP BY Payment_Mode
ORDER BY orders DESC;

-- 9. Customers with highest recorded sales
SELECT Customer_Name, COUNT(DISTINCT Order_ID) AS orders,
       ROUND(SUM(Sales),2) AS recorded_sales
FROM sales
GROUP BY Customer_Name
ORDER BY recorded_sales DESC
LIMIT 10;

-- 10. Negative-profit transactions (investigate; do not delete)
SELECT Order_ID, Order_Date, Product, Category, Sales, Profit, Order_Status
FROM sales
WHERE Profit < 0
ORDER BY Profit ASC;

-- 11. Discount impact by discount band
SELECT Discount, COUNT(*) AS orders,
       ROUND(AVG(Sales),2) AS average_sales,
       ROUND(AVG(Profit),2) AS average_profit
FROM sales
GROUP BY Discount
ORDER BY Discount;

-- 12. City-level performance
SELECT City, State, COUNT(*) AS orders,
       ROUND(SUM(Sales),2) AS total_sales,
       ROUND(SUM(Profit),2) AS total_profit
FROM sales
GROUP BY City, State
ORDER BY total_sales DESC;

-- 13. Delivered / returned / cancelled order counts
SELECT Order_Status, COUNT(*) AS order_count
FROM sales
GROUP BY Order_Status;

-- 14. Data quality checks
SELECT COUNT(*) AS rows_loaded,
       COUNT(DISTINCT Order_ID) AS unique_order_ids,
       SUM(Order_ID IS NULL) AS null_order_ids,
       SUM(Order_Date IS NULL) AS null_order_dates
FROM sales;

-- NOTE:
-- The source dataset has no separate refund/return-value field.
-- Sales is reported as recorded in the source. Do not label it "net revenue"
-- or assume returned-order sales have already been deducted.
