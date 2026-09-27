# Architecture

BioVerity is organized around five core records:

- EOR: Ecological Observation Record
- EER: Ecological Evidence Record
- ECR: Ecological Claim Record
- EDR: Ecological Decision Record
- EIR: Ecological Investigation Record

Generative systems may propose, extract, or summarize. VerityDecision scores, classifies, and ranks. The policy engine authorizes software action. Humans approve consequential scientific or management action.

## MVP Flow

```text
Observation
→ Evidence
→ Claim
→ Claim CI
→ Investigation
→ VerityDecision
→ Policy
→ Human Review
→ Claim Revision
```

