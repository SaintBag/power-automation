# Semantic Model → SQL Mapping

This document defines the explicit mapping between the semantic model
(`metadata/model.example.yml`) and the SQL implementation.

Its purpose is to guarantee:
- determinism,
- auditability,
- compatibility with automated validation and generation.

---

## FACT TABLES

### fact_sales

**Grain**  
OrderID + ProductID

**SQL Implementation**  
`sql/fact/fact_sales.sql`

| Semantic Field | SQL Column   | Source Table |
|---------------|-------------|--------------|
| order_id      | OrderID     | sales_data  |
| product_id    | ProductID   | sales_data  |
| customer_key  | CustomerID  | sales_data  |
| order_date    | OrderDate   | sales_data  |
| quantity      | Quantity    | sales_data  |
| unit_price    | UnitPrice   | sales_data  |
| total_amount  | TotalAmount | sales_data  |

---

## DIMENSIONS

### dim_customer

**Grain**  
1 row per CustomerID

**SQL Implementation**  
`sql/dim/dim_customer.sql`

| Semantic Field | SQL Column    | Source Table |
|---------------|--------------|--------------|
| customer_key  | CustomerID   | sales_data  |
| customer_name | CustomerName | sales_data  |
| region        | Region       | sales_data  |

---

### dim_product

**Grain**  
1 row per ProductID

**SQL Implementation**  
`sql/dim/dim_product.sql`

| Semantic Field | SQL Column   | Source Table |
|---------------|-------------|--------------|
| product_key   | ProductID   | sales_data  |
| product_name  | ProductName | sales_data  |

---

### dim_date

**Status**  
Deferred

**Rationale**  
Date dimension will be generated explicitly as a calendar table
at a later stage to support fiscal logic and time intelligence.

Currently, `OrderDate` is modeled as a fact attribute.
