# ADR-0002: Use PostgreSQL and PostGIS

## Status

Accepted

## Context

BioVerity stores ecological observations with geospatial context and provenance.

## Decision

Use PostgreSQL with PostGIS for the local MVP database.

## Consequences

The repository can support geospatial queries without introducing a separate graph or search database in the foundation.

