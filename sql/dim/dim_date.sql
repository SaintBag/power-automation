CREATE OR REPLACE VIEW dim_date AS
SELECT DISTINCT
    sd.OrderDate AS order_date
FROM sales_data sd
WHERE sd.OrderDate IS NOT NULL;
