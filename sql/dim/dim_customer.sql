CREATE OR REPLACE VIEW dim_customer AS
SELECT DISTINCT
    sd.CustomerID   AS customer_id,
    sd.CustomerName AS customer_name,
    sd.Region       AS region
FROM sales_data sd
WHERE sd.CustomerID IS NOT NULL;

