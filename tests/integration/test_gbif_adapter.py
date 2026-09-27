from bioverity.ingestion.adapters import GbifAdapter


def test_gbif_normalize_preserves_source_and_location() -> None:
    observation = GbifAdapter().normalize(
        {
            "key": "123",
            "taxonKey": "456",
            "eventDate": "2026-04-12T14:20:00Z",
            "decimalLatitude": 38.91,
            "decimalLongitude": -77.04,
            "coordinateUncertaintyInMeters": 100,
            "confidence": 0.91,
            "ecoregion": "mid-atlantic",
            "retrieved_at": "2026-09-27T00:00:00Z",
            "quality_flags": ["georeferenced"],
        }
    )

    assert observation.observation_id == "EOR-123"
    assert observation.species_id == "taxon:456"
    assert observation.source.provider == "gbif"
    assert observation.location.ecoregion == "mid-atlantic"
    assert observation.provenance.source_identifier == "123"
    assert observation.provenance.pipeline_version == "gbif-adapter-0.1.0"
    assert observation.provenance.quality_flags == ["georeferenced"]
