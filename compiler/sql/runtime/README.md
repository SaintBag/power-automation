# SQL Compiler Runtime

This directory defines the SQL Intermediate Representation (SQL IR).

Properties of SQL IR:
- dialect-agnostic
- immutable
- deterministic
- formatting-independent

SQL IR is the only structure consumed by SQL compiler passes.