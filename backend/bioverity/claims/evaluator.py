from __future__ import annotations

from bioverity.schemas.records import (
    ClaimEvaluation,
    ClaimStatus,
    EcologicalClaim,
    EcologicalEvidence,
    EvidenceDirection,
    EvidenceSnapshot,
)

EVALUATION_VERSION = "claim-ci-0.1.0"


def weighted_support(evidence: list[EcologicalEvidence]) -> tuple[float, float]:
    if not evidence:
        return 0.0, 1.0

    weighted_total = 0.0
    quality_total = 0.0
    for item in evidence:
        sign = -1 if item.direction == EvidenceDirection.CONTRADICTING else 1
        contribution = sign * item.strength * item.quality_score
        weighted_total += contribution
        quality_total += item.quality_score

    normalized = (weighted_total / quality_total + 1) / 2 if quality_total else 0
    support = min(1.0, max(0.0, normalized))
    uncertainty = min(1.0, max(0.05, 1 / (len(evidence) + quality_total)))
    return round(support, 4), round(uncertainty, 4)


def classify_claim(support: float, uncertainty: float, min_evidence_met: bool) -> ClaimStatus:
    if not min_evidence_met or uncertainty >= 0.55:
        return ClaimStatus.INSUFFICIENT_EVIDENCE
    if support >= 0.7:
        return ClaimStatus.SUPPORTED
    if support <= 0.35:
        return ClaimStatus.CONTRADICTED
    return ClaimStatus.DRIFTING


def evaluate_claim(
    claim: EcologicalClaim,
    evidence: list[EcologicalEvidence],
    snapshot: EvidenceSnapshot,
    regression_threshold: float = 0.15,
    minimum_evidence: int = 2,
) -> ClaimEvaluation:
    support_after, uncertainty = weighted_support(evidence)
    min_evidence_met = len(evidence) >= minimum_evidence
    status_after = classify_claim(support_after, uncertainty, min_evidence_met)
    delta = round(support_after - claim.support_score, 4)
    regression_detected = (
        abs(delta) >= regression_threshold
        and min_evidence_met
        and status_after in {ClaimStatus.DRIFTING, ClaimStatus.CONTRADICTED}
    )
    return ClaimEvaluation(
        claim_id=claim.claim_id,
        status_before=claim.status,
        status_after=status_after,
        support_before=claim.support_score,
        support_after=support_after,
        delta=delta,
        uncertainty=uncertainty,
        evidence_snapshot=snapshot.snapshot_id,
        evaluation_version=EVALUATION_VERSION,
        regression_detected=regression_detected,
    )
