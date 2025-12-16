-- Dimension: Customer
-- Grain: 1 row per CustomerID

CREATE OR REPLACE VIEW dim_customer AS
SELECT DISTINCT
    CustomerID      AS customer_key,
    CustomerName    AS customer_name,
    Region           AS region
FROM sales_data
WHERE CustomerID IS NOT NULL;
