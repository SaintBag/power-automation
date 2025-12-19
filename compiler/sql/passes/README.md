# SQL Compiler Passes

This directory contains SQL compiler passes.

Each pass:
- accepts SQL IR
- returns SQL IR
- is deterministic
- has a single responsibility

## Implemented Passes

- NormalizeFactQueryPass  
  Normalizes generic SQL IR into a fact-aware SQL query structure.
- BindMeasureAggregationPass  
  Attaches deterministic aggregation semantics to fact measures.
- BindDimensionJoinsPass  
  Binds dimension join and projection semantics to fact queries.