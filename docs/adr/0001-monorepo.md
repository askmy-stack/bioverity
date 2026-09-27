# ADR-0001: Use a Monorepo

## Status

Accepted

## Context

The MVP needs backend schemas, API code, fixtures, evaluation scripts, and a presentable frontend shell to evolve together.

## Decision

Use a single `bioverity` monorepo.

## Consequences

Shared schemas and fixtures stay close to implementation. Larger service boundaries are deferred until justified.

