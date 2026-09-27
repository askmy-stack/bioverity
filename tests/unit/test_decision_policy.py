from bioverity.decisions.verity import decide_change, decide_evidence
from bioverity.policies.engine import PolicyContext, evaluate_policy
from bioverity.schemas.records import ClaimEvaluation, ClaimStatus


def test_regression_routes_to_investigation_and_policy_review() -> None:
    evaluation = ClaimEvaluation(
        claim_id="ECR-1",
        status_before=ClaimStatus.SUPPORTED,
        status_after=ClaimStatus.DRIFTING,
        support_before=0.82,
        support_after=0.58,
        delta=-0.24,
        uncertainty=0.2,
        evidence_snapshot="EVS-1",
        evaluation_version="claim-ci-0.1.0",
        regression_detected=True,
    )
    decision = decide_evidence("ECR-1", "EVS-1", evaluation)
    policy = {
        "policy_id": "POL-1",
        "when": {
            "decision_type": "next_evidence",
            "investigate_probability_gte": 0.65,
            "minimum_observations": 100,
            "independent_sources_gte": 2,
        },
        "then": {"action": "open_investigation"},
        "otherwise": {"action": "require_researcher_review"},
    }

    assert decide_change(evaluation) == "investigate"
    assert decision.selected_action == "field_survey"
    assert decision.requires_human_review is True
    assert (
        evaluate_policy(policy, decision, PolicyContext(3, 2)).action == "require_researcher_review"
    )
