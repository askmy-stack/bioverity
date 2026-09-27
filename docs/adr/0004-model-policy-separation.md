# ADR-0004: Separate Model Judgment from Policy

## Status

Accepted

## Context

VerityDecision should rank and classify, but should not authorize consequential action.

## Decision

Model outputs flow into a deterministic policy engine before software action.

## Consequences

Thresholds and authorization rules are versioned, testable, and auditable outside model code.

