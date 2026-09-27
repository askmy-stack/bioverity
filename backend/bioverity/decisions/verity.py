from __future__ import annotations

from bioverity.schemas.records import ClaimEvaluation, EcologicalDecision


def decide_claim(evaluation: ClaimEvaluation) -> str:
    return evaluation.status_after.value


def decide_change(evaluation: ClaimEvaluation) -> str:
    if evaluation.regression_detected and evaluation.delta <= -0.3:
        return "urgent_review"
    if evaluation.regression_detected:
        return "investigate"
    if abs(evaluation.delta) >= 0.08:
        return "watch"
    return "normal"


def decide_evidence(
    claim_id: str, snapshot_id: str, evaluation: ClaimEvaluation
) -> EcologicalDecision:
    if evaluation.regression_detected:
        actions = {
            "field_survey": 0.46,
            "climate_sampling": 0.24,
            "literature_review": 0.14,
            "remote_sensing_review": 0.10,
            "expert_review": 0.05,
            "no_action": 0.01,
        }
    elif evaluation.uncertainty >= 0.5:
        actions = {
            "literature_review": 0.34,
            "expert_review": 0.24,
            "field_survey": 0.18,
            "climate_sampling": 0.12,
            "remote_sensing_review": 0.08,
            "no_action": 0.04,
        }
    else:
        actions = {
            "no_action": 0.42,
            "literature_review": 0.18,
            "remote_sensing_review": 0.15,
            "field_survey": 0.12,
            "expert_review": 0.08,
            "climate_sampling": 0.05,
        }

    selected_action = max(actions, key=actions.get)
    return EcologicalDecision(
        decision_id="EDR-DEMO-001",
        claim_id=claim_id,
        decision_type="next_evidence",
        candidate_actions=actions,
        selected_action=selected_action,
        confidence=round(actions[selected_action], 4),
        requires_human_review=selected_action != "no_action",
        evidence_snapshot_id=snapshot_id,
    )


def decide_review(decision: EcologicalDecision) -> str:
    if decision.requires_human_review and decision.confidence >= 0.4:
        return "researcher"
    if decision.requires_human_review:
        return "domain_expert"
    return "automatic"


def decide_stop(evaluation: ClaimEvaluation) -> str:
    if evaluation.regression_detected or evaluation.uncertainty > 0.3:
        return "continue_investigation"
    return "evidence_sufficient"
