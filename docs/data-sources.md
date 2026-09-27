# Data Sources

The MVP adapter surface is designed for GBIF, iNaturalist, NOAA, ERA5, USGS, EPA ecoregions, OpenAlex, and Crossref.

Only the GBIF normalization adapter is implemented in the repository foundation. Network fetching is deferred until the first ingestion sprint so the initial repo remains testable offline.

## Observation Provenance

Every EOR includes a `provenance` object with the source provider and identifier, retrieval time, ordered transformation steps, pipeline version, and quality flags. The provider and identifier must match the observation's `source` reference. The retrieval time includes a timezone. The [valid demo observations](../datasets/fixtures/demo_observations.json) and [invalid example](../datasets/fixtures/invalid_observation_provenance.json) exercise the [EOR JSON Schema](../specs/eor.schema.json) and Pydantic model in contract tests.
