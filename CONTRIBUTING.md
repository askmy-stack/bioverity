# Contributing

BioVerity is early-stage open scientific infrastructure. Contributions should keep the MVP small, deterministic, and auditable.

## Principles

- Preserve provenance through every transformation.
- Keep model judgment, policy authorization, and human authority separate.
- Prefer interpretable baselines before complex models.
- Do not allow generated text to directly mutate accepted scientific claims.
- Every scientific feature needs tests, documentation, and reproducibility.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check .
ruff format --check .
```

