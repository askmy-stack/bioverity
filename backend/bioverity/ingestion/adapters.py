from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Protocol

from bioverity.schemas.records import (
    EcologicalObservation,
    Location,
    ObservationProvenance,
    Quality,
    SourceRef,
)


@dataclass(frozen=True)
class ObservationQuery:
    taxon: str
    min_lat: float
    min_lon: float
    max_lat: float
    max_lon: float
    start_date: datetime
    end_date: datetime


class ObservationAdapter(Protocol):
    def fetch(self, query: ObservationQuery) -> list[dict[str, Any]]: ...

    def normalize(self, raw: dict[str, Any]) -> EcologicalObservation: ...


class GbifAdapter:
    provider = "gbif"

    def fetch(self, query: ObservationQuery) -> list[dict[str, Any]]:
        raise NotImplementedError(
            "Network fetching is intentionally deferred from the MVP scaffold."
        )

    def normalize(self, raw: dict[str, Any]) -> EcologicalObservation:
        source_id = str(raw["key"])
        return EcologicalObservation(
            observation_id=f"EOR-{raw['key']}",
            species_id=f"taxon:{raw['taxonKey']}",
            observed_at=datetime.fromisoformat(raw["eventDate"]),
            location=Location(
                lat=float(raw["decimalLatitude"]),
                lon=float(raw["decimalLongitude"]),
                ecoregion=raw.get("ecoregion", "mid-atlantic"),
            ),
            source=SourceRef(provider=self.provider, source_id=source_id),
            quality=Quality(
                coordinate_uncertainty_m=float(raw.get("coordinateUncertaintyInMeters", 1000)),
                confidence=float(raw.get("confidence", 0.8)),
            ),
            provenance=ObservationProvenance(
                source_provider=self.provider,
                source_identifier=source_id,
                retrieved_at=datetime.fromisoformat(raw["retrieved_at"])
                if raw.get("retrieved_at")
                else datetime.now(UTC),
                transformation_steps=["gbif.normalize:v1"],
                pipeline_version="gbif-adapter-0.1.0",
                quality_flags=list(raw.get("quality_flags", [])),
            ),
        )
