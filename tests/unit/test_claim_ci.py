from bioverity.claims.evaluator import evaluate_claim
from bioverity.schemas.records import (
    ClaimAssertion,
    ClaimContext,
    ClaimStatus,
    EcologicalClaim,
    EcologicalEvidence,
    EvidenceDirection,
    EvidenceSnapshot,
    ExpectedRelationship,
    Provenance,
)


def test_claim_ci_is_deterministic_for_same_snapshot() -> None:
    claim = EcologicalClaim(
        claim_id="ECR-1",
        version=1,
        assertion=ClaimAssertion(
            subject="species:a", relation="interacts_with", object="species:b"
        ),
        context=ClaimContext(region="mid-atlantic"),
        expected_relationship=ExpectedRelationship(driver="temperature", direction="positive"),
        status=ClaimStatus.SUPPORTED,
        support_score=0.82,
        uncertainty=0.12,
    )
    evidence = [
        EcologicalEvidence(
            evidence_id="EER-1",
            claim_id="ECR-1",
            evidence_type="field_observation",
            direction=EvidenceDirection.SUPPORTING,
            source_ids=["EOR-1"],
            strength=0.76,
            quality_score=0.86,
            provenance=Provenance(pipeline_version="0.1.0"),
        ),
        EcologicalEvidence(
            evidence_id="EER-2",
            claim_id="ECR-1",
            evidence_type="field_observation",
            direction=EvidenceDirection.CONTRADICTING,
            source_ids=["EOR-2"],
            strength=0.42,
            quality_score=0.82,
            provenance=Provenance(pipeline_version="0.1.0"),
        ),
    ]
    snapshot = EvidenceSnapshot(
        snapshot_id="EVS-1",
        claim_id="ECR-1",
        evidence_ids=["EER-2", "EER-1"],
    )

    first = evaluate_claim(claim, evidence, snapshot)
    second = evaluate_claim(claim, evidence, snapshot)

    assert first == second
    assert snapshot.evidence_ids == ["EER-1", "EER-2"]
