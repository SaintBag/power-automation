# Compiler Layer

This directory defines the **semantic compiler** responsible for transforming
validated semantic contracts into deterministic output artifacts.

## Responsibilities

The compiler layer:
- consumes the semantic contract (`semantic/model.contract.yml`)
- applies deterministic transformation passes
- produces generated artifacts in `output/`

The compiler **never**:
- reads data
- connects to external systems
- mutates source-of-truth inputs

## Architecture

The compiler is structured as a pipeline of explicit passes.

### passes/

Each pass:
- has a single responsibility
- is deterministic
- produces a well-defined intermediate representation (IR)

Examples (future):
- semantic normalization
- grain resolution
- join inference
- SQL rendering

### runtime/

Runtime utilities shared across passes:
- error handling
- IR definitions
- compiler context

## Status

This directory currently defines **structure and intent only**.
No executable logic is implemented at this stage.