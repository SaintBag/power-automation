# SQL Compiler Layer

This directory defines the SQL backend of the compiler.

Responsibilities:
- consume SemanticModelIR
- produce SQL Intermediate Representation (SQL IR)
- apply deterministic SQL compiler passes

Non-responsibilities:
- no SQL string rendering
- no filesystem writes
- no database access

This layer defines how semantic concepts are mapped to SQL constructs.