# Prompts

This directory contains prompt definitions used by the LLM
during the data model automation process.

Each prompt has a single responsibility, such as:
- analytical model design (facts, dimensions, grain)
- SQL generation
- model validation

Prompts are treated as versioned code and are executed in CI/CD.
