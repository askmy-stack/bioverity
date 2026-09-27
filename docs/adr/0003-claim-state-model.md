# ADR-0003: Use Four Claim States

## Status

Accepted

## Context

Claim CI needs explicit, auditable output states.

## Decision

Use `supported`, `drifting`, `contradicted`, and `insufficient_evidence`.

## Consequences

The evaluator can abstain when evidence is weak instead of inventing certainty.

