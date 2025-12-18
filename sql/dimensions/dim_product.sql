CREATE OR REPLACE VIEW dim_product AS
SELECT DISTINCT
    sd.ProductID   AS product_id,
    sd.ProductName AS product_name
FROM sales_data sd