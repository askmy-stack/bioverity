from __future__ import annotations

from bioverity.claims.evaluator import evaluate_claim
from bioverity.core.config import settings
from bioverity.db.health import database_healthy
from bioverity.decisions.verity import decide_change, decide_evidence
from bioverity.policies.engine import PolicyContext, evaluate_policy, load_policy
from bioverity.schemas.records import (
    EcologicalClaim,
    EcologicalDecision,
    EcologicalEvidence,
    EcologicalObservation,
    EvidenceSnapshot,
    PolicyDecision,
)
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

app = FastAPI(title="BioVerity", version="0.1.0")

OBSERVATIONS: dict[str, EcologicalObservation] = {}
EVIDENCE: dict[str, EcologicalEvidence] = {}
CLAIMS: dict[str, EcologicalClaim] = {}


@app.get("/health")
def health() -> dict[str, str]:
    try:
        engine = create_engine(settings.database_url)
        try:
            database_healthy(engine)
        finally:
            engine.dispose()
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return {"status": "ok", "database": "ok"}


@app.post("/v1/observations", response_model=EcologicalObservation)
def create_observation(observation: EcologicalObservation) -> EcologicalObservation:
    OBSERVATIONS[observation.observation_id] = observation
    return observation


@app.get("/v1/observations", response_model=list[EcologicalObservation])
def list_observations() -> list[EcologicalObservation]:
    return list(OBSERVATIONS.values())


@app.get("/v1/observations/{observation_id}", response_model=EcologicalObservation)
def get_observation(observation_id: str) -> EcologicalObservation:
    return OBSERVATIONS[observation_id]


@app.post("/v1/evidence", response_model=EcologicalEvidence)
def create_evidence(evidence: EcologicalEvidence) -> EcologicalEvidence:
    EVIDENCE[evidence.evidence_id] = evidence
    return evidence


@app.get("/v1/evidence/{evidence_id}", response_model=EcologicalEvidence)
def get_evidence(evidence_id: str) -> EcologicalEvidence:
    return EVIDENCE[evidence_id]


@app.get("/v1/claims/{claim_id}/evidence", response_model=list[EcologicalEvidence])
def list_claim_evidence(claim_id: str) -> list[EcologicalEvidence]:
    return [item for item in EVIDENCE.values() if item.claim_id == claim_id]


@app.post("/v1/claims", response_model=EcologicalClaim)
def create_claim(claim: EcologicalClaim) -> EcologicalClaim:
    CLAIMS[claim.claim_id] = claim
    return claim


@app.get("/v1/claims", response_model=list[EcologicalClaim])
def list_claims() -> list[EcologicalClaim]:
    return list(CLAIMS.values())


@app.get("/v1/claims/{claim_id}", response_model=EcologicalClaim)
def get_claim(claim_id: str) -> EcologicalClaim:
    return CLAIMS[claim_id]


@app.post("/v1/claims/{claim_id}/evaluate")
def evaluate_claim_endpoint(claim_id: str) -> dict[str, object]:
    claim = CLAIMS[claim_id]
    evidence = list_claim_evidence(claim_id)
    snapshot = EvidenceSnapshot(
        snapshot_id=f"EVS-{claim_id}",
        claim_id=claim_id,
        evidence_ids=[item.evidence_id for item in evidence],
    )
    evaluation = evaluate_claim(claim, evidence, snapshot)
    return {
        "snapshot": snapshot,
        "evaluation": evaluation,
        "change_decision": decide_change(evaluation),
    }


@app.post("/v1/decisions/evidence", response_model=EcologicalDecision)
def evidence_decision(evaluation: dict[str, object]) -> EcologicalDecision:
    claim_id = str(evaluation["claim_id"])
    snapshot_id = str(evaluation["evidence_snapshot"])
    claim = CLAIMS[claim_id]
    evidence = list_claim_evidence(claim_id)
    typed_eval = evaluate_claim(
        claim,
        evidence,
        EvidenceSnapshot(
            snapshot_id=snapshot_id,
            claim_id=claim_id,
            evidence_ids=[item.evidence_id for item in evidence],
        ),
    )
    return decide_evidence(claim_id, snapshot_id, typed_eval)


@app.post("/v1/policies/evaluate", response_model=PolicyDecision)
def policy_decision(decision: EcologicalDecision) -> PolicyDecision:
    policy = load_policy("policies/investigate.yaml")
    return evaluate_policy(
        policy, decision, PolicyContext(minimum_observations=3, independent_sources=2)
    )
