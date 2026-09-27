from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class ClaimStatus(StrEnum):
    SUPPORTED = "supported"
    DRIFTING = "drifting"
    CONTRADICTED = "contradicted"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class EvidenceDirection(StrEnum):
    SUPPORTING = "supporting"
    CONTRADICTING = "contradicting"
    CONTEXTUAL = "contextual"


class Location(BaseModel):
    lat: float = Field(ge=-90, le=90)
    lon: float = Field(ge=-180, le=180)
    ecoregion: str


class SourceRef(BaseModel):
    provider: str
    source_id: str


class Quality(BaseModel):
    coordinate_uncertainty_m: float = Field(ge=0)
    confidence: float = Field(ge=0, le=1)


class Provenance(BaseModel):
    pipeline_version: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_provider: str | None = None
    source_identifier: str | None = None
    transformation_steps: list[str] = Field(default_factory=list)
    quality_flags: list[str] = Field(default_factory=list)


class ObservationProvenance(BaseModel):
    source_provider: str = Field(min_length=1)
    source_identifier: str = Field(min_length=1)
    retrieved_at: datetime
    transformation_steps: list[str]
    pipeline_version: str = Field(min_length=1)
    quality_flags: list[str]

    @field_validator("retrieved_at")
    @classmethod
    def retrieved_at_has_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("retrieved_at must include a timezone")
        return value


class EcologicalObservation(BaseModel):
    observation_id: str
    species_id: str
    observed_at: datetime
    location: Location
    source: SourceRef
    quality: Quality
    provenance: ObservationProvenance

    @model_validator(mode="after")
    def source_matches_provenance(self) -> EcologicalObservation:
        if (
            self.source.provider != self.provenance.source_provider
            or self.source.source_id != self.provenance.source_identifier
        ):
            raise ValueError("observation source and provenance source must match")
        return self


class EcologicalEvidence(BaseModel):
    evidence_id: str
    claim_id: str
    evidence_type: str
    direction: EvidenceDirection
    source_ids: list[str]
    strength: float = Field(ge=0, le=1)
    quality_score: float = Field(ge=0, le=1)
    provenance: Provenance


class ClaimAssertion(BaseModel):
    subject: str
    relation: str
    object: str


class ClaimContext(BaseModel):
    region: str
    season: str | None = None


class ExpectedRelationship(BaseModel):
    driver: str
    direction: Literal["positive", "negative", "neutral", "unknown"]


class EcologicalClaim(BaseModel):
    claim_id: str
    version: int = Field(ge=1)
    assertion: ClaimAssertion
    context: ClaimContext
    expected_relationship: ExpectedRelationship
    status: ClaimStatus
    support_score: float = Field(ge=0, le=1)
    uncertainty: float = Field(ge=0, le=1)
    last_tested_at: datetime | None = None


class EvidenceSnapshot(BaseModel):
    snapshot_id: str
    claim_id: str
    evidence_ids: list[str]
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    snapshot_version: str = "evidence-snapshot-0.1.0"

    @field_validator("evidence_ids")
    @classmethod
    def evidence_ids_are_sorted(cls, value: list[str]) -> list[str]:
        return sorted(value)


class ClaimEvaluation(BaseModel):
    claim_id: str
    status_before: ClaimStatus
    status_after: ClaimStatus
    support_before: float = Field(ge=0, le=1)
    support_after: float = Field(ge=0, le=1)
    delta: float
    uncertainty: float = Field(ge=0, le=1)
    evidence_snapshot: str
    evaluation_version: str
    regression_detected: bool


class Hypothesis(BaseModel):
    hypothesis_id: str
    description: str
    predictions: list[str]
    required_evidence: list[str]
    supporting_evidence: list[str] = Field(default_factory=list)
    contradicting_evidence: list[str] = Field(default_factory=list)
    uncertainty: float = Field(ge=0, le=1)


class EcologicalInvestigation(BaseModel):
    investigation_id: str
    claim_id: str
    trigger: str
    opened_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    status: Literal["active", "closed", "paused"]
    hypotheses: list[Hypothesis]


class EcologicalDecision(BaseModel):
    decision_id: str
    claim_id: str
    decision_type: str
    candidate_actions: dict[str, float]
    selected_action: str
    confidence: float = Field(ge=0, le=1)
    requires_human_review: bool
    evidence_snapshot_id: str
    model_version: str = "veritydecision-0.1.0"
    policy_version: str = "policy-0.1.0"


class PolicyDecision(BaseModel):
    policy_id: str
    action: str
    authorized: bool
    reason: str
