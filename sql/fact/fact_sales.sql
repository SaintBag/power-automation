-- fact_sales
-- Grain: 1 row per OrderID
-- Source: sales_data
-- Conformed for Power BI (Import / DirectQuery safe)

CREATE OR REPLACE VIEW fact_sales AS
SELECT
    sd.OrderID            AS order_id,

    -- Foreign keys
    sd.CustomerID         AS customer_id,
    sd.ProductID          AS product_id,
    sd.OrderDate          AS order_date,

    -- Measures
    CAST(sd.Quantity AS INT)               AS quantity,
    CAST(sd.TotalAmount AS DECIMAL(12,2))  AS total_amount

FROM sales_data sd;