-- Dimension: Product
-- Grain: 1 row per ProductID

CREATE OR REPLACE VIEW dim_product AS
SELECT DISTINCT
    ProductID     AS product_key,
    ProductName   AS product_name
FROM sales_data
WHERE ProductID IS NOT NULL;
