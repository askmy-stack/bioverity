from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from bioverity.schemas.records import EcologicalDecision, PolicyDecision


@dataclass(frozen=True)
class PolicyContext:
    minimum_observations: int
    independent_sources: int


def load_policy(path: str | Path) -> dict[str, Any]:
    with Path(path).open() as handle:
        loaded = yaml.safe_load(handle)
    if not isinstance(loaded, dict):
        raise TypeError("Policy file must contain a mapping.")
    return loaded


def evaluate_policy(
    policy: dict[str, Any], decision: EcologicalDecision, context: PolicyContext
) -> PolicyDecision:
    when = policy.get("when", {})
    threshold = float(when.get("investigate_probability_gte", 1))
    minimum_observations = int(when.get("minimum_observations", 0))
    independent_sources = int(when.get("independent_sources_gte", 0))

    selected_probability = decision.candidate_actions.get(decision.selected_action, 0)
    matched = (
        decision.decision_type == when.get("decision_type")
        and selected_probability >= threshold
        and context.minimum_observations >= minimum_observations
        and context.independent_sources >= independent_sources
    )

    action = policy["then"]["action"] if matched else policy["otherwise"]["action"]
    return PolicyDecision(
        policy_id=policy["policy_id"],
        action=action,
        authorized=matched,
        reason="Policy conditions satisfied." if matched else "Policy conditions not satisfied.",
    )
