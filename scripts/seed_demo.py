from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from bioverity.claims.evaluator import evaluate_claim
from bioverity.decisions.verity import decide_change, decide_evidence, decide_review, decide_stop
from bioverity.policies.engine import PolicyContext, evaluate_policy, load_policy
from bioverity.schemas.records import EcologicalClaim, EcologicalEvidence, EvidenceSnapshot


def load_json(path: str):
    with (ROOT / path).open() as handle:
        return json.load(handle)


def main() -> None:
    claim = EcologicalClaim.model_validate(load_json("datasets/fixtures/demo_claim.json"))
    evidence = [
        EcologicalEvidence.model_validate(item)
        for item in load_json("datasets/fixtures/demo_evidence.json")
    ]
    snapshot = EvidenceSnapshot(
        snapshot_id="EVS-000021",
        claim_id=claim.claim_id,
        evidence_ids=[item.evidence_id for item in evidence],
    )
    evaluation = evaluate_claim(claim, evidence, snapshot)
    decision = decide_evidence(claim.claim_id, snapshot.snapshot_id, evaluation)
    policy = evaluate_policy(
        load_policy(ROOT / "policies/investigate.yaml"),
        decision,
        PolicyContext(minimum_observations=3, independent_sources=2),
    )

    result = {
        "claim_id": claim.claim_id,
        "change": decide_change(evaluation),
        "evaluation": evaluation.model_dump(mode="json"),
        "decision": decision.model_dump(mode="json"),
        "review": decide_review(decision),
        "stop": decide_stop(evaluation),
        "policy": policy.model_dump(mode="json"),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
