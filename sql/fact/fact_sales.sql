CREATE OR REPLACE VIEW fact_sales AS
SELECT
    sd.OrderID      AS order_id,

    -- Foreign keys
    sd.CustomerID   AS customer_id,
    sd.ProductID    AS product_id,
    sd.OrderDate    AS order_date,

    -- Measures (AGGREGATED)
    SUM(sd.Quantity)      AS quantity,
    SUM(sd.TotalAmount)   AS total_amount
FROM sales_data sd
GROUP BY
    sd.OrderID,
    sd.CustomerID,
    sd.ProductID,
    sd.OrderDate;
