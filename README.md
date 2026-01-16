# PromptShield

PromptShield is a CI/CD-integrated LLM Security Gate that runs adversarial
tests against your model configuration and returns a binary pass/fail verdict
based on a configurable security score.

## Quick Start

1) Create a config (or use the included `promptshield.yaml`)
2) Run a scan

```
promptshield scan --config promptshield.yaml --output-dir artifacts
```

## Tests

```
make setup
make test
```

## What This MVP Includes

- Static regression probes (Garak-style)
- Adaptive red teaming (PyRIT-style)
- Guardrail validation (LLM Guard via library integration)
- Safety judge scoring and CI-friendly verdicts
- JSON artifacts with transcripts and score breakdown

## Repo Layout

- `src/promptshield/cli.py` – CLI entrypoint
- `src/promptshield/runner.py` – Orchestration
- `src/promptshield/engines/` – Attack engines
- `src/promptshield/guard/` – Guard wrappers
- `src/promptshield/judge/` – Safety judge
- `promptshield.yaml` – Example config

## Notes

This scaffold integrates Garak, PyRIT, and LLM Guard as libraries. The example
config uses LLM Guard scanners and library-backed attack engines. If you prefer
the built-in deterministic probes, set `attacks.garak.mode` or
`attacks.pyrit.mode` to `builtin`.

