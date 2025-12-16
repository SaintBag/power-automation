-- Fact: Sales
-- Grain: OrderID + ProductID

CREATE OR REPLACE VIEW fact_sales AS
SELECT
    OrderID        AS order_id,
    ProductID      AS product_id,
    CustomerID     AS customer_key,
    OrderDate      AS order_date,
    Quantity       AS quantity,
    UnitPrice      AS unit_price,
    TotalAmount    AS total_amount
FROM sales_data
WHERE OrderID IS NOT NULL
  AND ProductID IS NOT NULL;
