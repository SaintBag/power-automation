# SQL Renderers

This package contains deterministic SQL renderers.

Responsibilities:
- Transform fully-resolved SQL IR into SQL strings
- No semantic decisions
- No database access
- No dialect-specific logic (foundations only)

Current renderers:
- FactQueryRenderer