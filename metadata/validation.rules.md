# Semantic Model Validation Rules

This document defines structural validation rules for the analytical model.
Rules are evaluated without accessing data.

---

## Rule 1 — Fact Grain Uniqueness

Each fact table must declare a grain composed of one or more columns.
All non-measure columns must be functionally dependent on the grain.

### Applies to
- fact_sales

### Grain
- order_id
- product_id

---

## Rule 2 — Fact-to-Dimension Relationships

Each foreign key in a fact table must reference exactly one dimension
with a unique primary key.

### fact_sales

| Fact Column  | Dimension     | Dimension Key |
|-------------|---------------|---------------|
| customer_key | dim_customer | customer_key |
| product_id   | dim_product  | product_key  |

---

## Rule 3 — No Many-to-Many Relationships

Dimensions must have unique keys.
Fact tables must not reference dimensions on non-unique attributes.

### Status
- PASS (by design)

---

## Rule 4 — Power BI Compatibility

The model must comply with Power BI constraints:
- no nested structures
- no arrays
- deterministic joins
- flat fact tables

### Status
- PASS
