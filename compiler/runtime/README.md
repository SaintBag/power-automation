# Compiler Runtime

This directory contains runtime contracts shared by compiler passes.

## Intermediate Representation (IR)

The IR defines the internal, normalized representation of the semantic model.

### Guarantees

- Immutable
- Fully validated before creation
- Free of source-system concerns
- Deterministic

### Purpose

Compiler passes operate **only** on the IR.
No pass reads raw YAML or SQL directly.

### Lifecycle

semantic contract (YAML)
→ validation
→ IR
→ compiler passes
→ output artifacts