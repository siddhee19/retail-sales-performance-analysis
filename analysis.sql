/* =========================================================
   RETAIL SALES PERFORMANCE ANALYSIS
   Dataset: Sample Superstore (2014-2017, 9,994 orders)
   Table: orders (cleaned - see data_cleaning notes in README)
   ========================================================= */


/* -----------------------------------------------------------
   Q1. Overall business snapshot
   What's the total scale of the business?
----------------------------------------------------------- */
SELECT
    COUNT(DISTINCT [Order ID])      AS total_orders,
    COUNT(*)                        AS total_line_items,
    ROUND(SUM(Sales), 2)            AS total_sales,
    ROUND(SUM(Profit), 2)           AS total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS overall_profit_margin_pct
FROM orders;


/* -----------------------------------------------------------
   Q2. Profitability by Region
   Which regions make money, and which underperform?
----------------------------------------------------------- */
SELECT
    Region,
    ROUND(SUM(Sales), 2)   AS total_sales,
    ROUND(SUM(Profit), 2)  AS total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct
FROM orders
GROUP BY Region
ORDER BY total_profit DESC;


/* -----------------------------------------------------------
   Q3. Profitability by Category and Sub-Category
   Category-level numbers can hide sub-category problems.
----------------------------------------------------------- */
SELECT
    Category,
    [Sub-Category],
    ROUND(SUM(Sales), 2)   AS total_sales,
    ROUND(SUM(Profit), 2)  AS total_profit,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct
FROM orders
GROUP BY Category, [Sub-Category]
ORDER BY total_profit ASC;   -- worst performers first


/* -----------------------------------------------------------
   Q4. Discount impact on profit
   Does heavier discounting actually hurt profitability?
----------------------------------------------------------- */
SELECT
    CASE
        WHEN Discount = 0 THEN '0% (no discount)'
        WHEN Discount <= 0.1 THEN '1-10%'
        WHEN Discount <= 0.2 THEN '11-20%'
        WHEN Discount <= 0.3 THEN '21-30%'
        ELSE '31%+'
    END AS discount_band,
    COUNT(*) AS num_orders,
    ROUND(SUM(Sales), 2)  AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(AVG(Profit), 2) AS avg_profit_per_order,
    ROUND(SUM(Profit) * 100.0 / SUM(Sales), 2) AS profit_margin_pct
FROM orders
GROUP BY discount_band
ORDER BY MIN(Discount);


/* -----------------------------------------------------------
   Q5. Top 10 most profitable products
----------------------------------------------------------- */
SELECT
    [Product Name],
    Category,
    [Sub-Category],
    ROUND(SUM(Sales), 2)  AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY [Product Name], Category, [Sub-Category]
ORDER BY total_profit DESC
LIMIT 10;


/* -----------------------------------------------------------
   Q6. Top 10 least profitable products (biggest money losers)
----------------------------------------------------------- */
SELECT
    [Product Name],
    Category,
    [Sub-Category],
    ROUND(SUM(Sales), 2)  AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(AVG(Discount), 2) AS avg_discount
FROM orders
GROUP BY [Product Name], Category, [Sub-Category]
ORDER BY total_profit ASC
LIMIT 10;


/* -----------------------------------------------------------
   Q7. Customer Segment performance
----------------------------------------------------------- */
SELECT
    Segment,
    COUNT(DISTINCT [Customer ID]) AS num_customers,
    ROUND(SUM(Sales), 2)  AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(SUM(Sales) / COUNT(DISTINCT [Customer ID]), 2) AS avg_sales_per_customer
FROM orders
GROUP BY Segment
ORDER BY total_profit DESC;


/* -----------------------------------------------------------
   Q8. Monthly sales trend (seasonality)
----------------------------------------------------------- */
SELECT
    [Order Year]  AS year,
    [Order Month] AS month,
    [Order Month Name] AS month_name,
    ROUND(SUM(Sales), 2)  AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit
FROM orders
GROUP BY year, month
ORDER BY year, month;


/* -----------------------------------------------------------
   Q9. Ship Mode usage and average shipping time
   (excludes rows flagged with invalid ship dates - see README)
----------------------------------------------------------- */
SELECT
    [Ship Mode],
    COUNT(*) AS num_orders,
    ROUND(AVG([Shipping Days]), 1) AS avg_shipping_days,
    ROUND(SUM(Sales), 2) AS total_sales
FROM orders
WHERE [Date Flag] = 'OK'
GROUP BY [Ship Mode]
ORDER BY avg_shipping_days;


/* -----------------------------------------------------------
   Q10. States with the highest losses
   Where should leadership investigate pricing/discount policy?
----------------------------------------------------------- */
SELECT
    State,
    Region,
    ROUND(SUM(Sales), 2)  AS total_sales,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(AVG(Discount), 2) AS avg_discount
FROM orders
GROUP BY State, Region
HAVING total_profit < 0
ORDER BY total_profit ASC;
