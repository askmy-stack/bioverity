export type ClaimStatus = "supported" | "drifting" | "contradicted" | "insufficient_evidence";

export interface ClaimSummary {
  claimId: string;
  status: ClaimStatus;
  supportScore: number;
  uncertainty: number;
  lastEvaluated: string;
}

