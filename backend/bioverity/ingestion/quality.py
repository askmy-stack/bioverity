from __future__ import annotations

from datetime import UTC, datetime

from bioverity.schemas.records import EcologicalObservation


def quality_flags(observation: EcologicalObservation) -> list[str]:
    flags: list[str] = []
    if observation.observed_at > datetime.now(UTC):
        flags.append("future_observation")
    if observation.quality.coordinate_uncertainty_m > 10_000:
        flags.append("high_coordinate_uncertainty")
    if not observation.species_id:
        flags.append("missing_taxonomy")
    return flags
