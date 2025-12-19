# Output — Generated Artifacts Only

This directory contains **only generated artifacts** produced by the automation pipeline.

## Rules (Non-Negotiable)

- No files in this directory are edited manually.
- All contents are generated deterministically from:
  - database schema (`schema/`)
  - semantic contract (`semantic/model.contract.yml`)
- Any manual change in this directory is considered invalid and must be overwritten.

## Purpose

Artifacts stored here are intended for direct consumption by downstream systems,
including Power BI.

Typical outputs include:
- Power BI–ready SQL views
- compiled fact and dimension definitions
- generated technical documentation

## Structure

- `sql/`  
  Generated SQL artifacts (facts, dimensions, views)

- `docs/`  
  Generated technical documentation

## Lifecycle

- This directory may be fully regenerated at any time.
- Git history is used only for auditability, not as a source of truth.

**Source of truth lives outside this directory.**