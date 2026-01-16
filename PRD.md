# PromptShield – Automated LLM Security Gate

## Product Requirements Document (PRD) & Technical Specification

---

## 1. Executive Summary

**PromptShield** is an automated, CI/CD-integrated **LLM Security Gate** that
continuously validates the safety and security posture of Large Language Model
(LLM) systems—especially system prompts and guardrails—before changes reach
production.

PromptShield functions as **SAST/DAST for LLM-powered applications**, enforcing
a quantifiable and repeatable security baseline by automatically attacking
models using known and adaptive techniques, objectively evaluating responses,
and issuing a **binary go/no-go decision** for every pull request.

PromptShield enables teams to move fast **without sacrificing AI safety**,
shifting LLM security left into the developer workflow.

---

## 2. Problem Statement

Modern LLM-powered systems evolve rapidly. Small, frequent changes—particularly
to system prompts—can silently reintroduce critical vulnerabilities such as:

- Prompt injection
- Jailbreaking
- Sensitive data (PII) leakage
- Toxic or harmful content generation
- Multi-turn social-engineering bypasses

Manual security validation does not scale with this pace. Existing runtime
guardrails are often insufficiently tested and may provide a false sense of
safety.

This creates a high-risk environment where:

- Development velocity conflicts with security
- Vulnerabilities escape into production
- Organizations lack objective, auditable proof of AI safety controls

---

## 3. Proposed Solution

PromptShield introduces a **mandatory automated security gate** enforced at
pull-request time.

On every PR that modifies LLM configuration (system prompts, policies, or
guardrails), PromptShield:

1. Executes **static and adaptive adversarial attacks**
2. Routes attacks through **intended production defenses**
3. Objectively evaluates model responses using a **Safety Judge LLM**
4. Generates a **composite Security Score**
5. Automatically **blocks or allows** the PR based on policy thresholds

This guarantees that no security regression can be merged unnoticed.

---

## 4. Target Users

### Primary Users

- **DevOps / MLOps Engineers** – CI/CD ownership and platform automation
- **AI Security Teams** – Policy definition, failure analysis, compliance

### Secondary Users

- Platform Engineering
- Risk, Audit, and Compliance

---

## 5. Product Goals & Success Metrics

### 5.1 Product Goals

1. **Automate LLM Security Regression Testing**
2. **Increase Developer Velocity with Safety Guarantees**
3. **Establish a Quantifiable, Enforceable Security Baseline**

### 5.2 Success Metrics

| Metric                     | Description                           |
| -------------------------- | ------------------------------------- |
| Security Score             | Composite score used for PR decisions |
| Vulnerability Hit Rate     | Number of successful attacks          |
| CI/CD Failure Rate         | % of PRs blocked                      |
| PII Leakage Detection Rate | Confirmed PII exposures               |
| Toxicity Severity Score    | Harmful content classification        |
| Refusal Quality Score      | Correctness of safe refusals          |

---

## 6. System Architecture

PromptShield is composed of **three core architectural pillars**.

### 6.1 Adversarial Engine (Attacker)

Responsible for generating and orchestrating attacks using:

- Static fuzzing (known vulnerabilities)
- Adaptive, multi-turn red teaming

### 6.2 Target Wrapper (Abstraction Layer)

Provides a unified interface to test:

- Local models (vLLM, Ollama)
- Hosted APIs (OpenAI, Anthropic, Azure)

### 6.3 Evaluation & Reporting Hub (Judge)

Classifies responses, calculates security metrics, and emits CI-compatible
verdicts.

---

## 7. Functional Requirements

### 7.1 Static Regression Scanning – Garak

**Purpose:** Prevent reintroduction of known vulnerabilities

- Execute 100+ predefined probes
- Deterministic execution
- Detect jailbreaks, injections, policy bypasses

Outputs structured vulnerability reports.

### 7.2 Adaptive Red-Teaming – PyRIT

**Purpose:** Identify novel and emergent vulnerabilities

Capabilities:

- Multi-turn conversational attacks
- Prompt mutation and obfuscation
- Social engineering simulations

An **Attack LLM** dynamically evolves attack strategies.

### 7.3 Guardrail Validation – LLM Guard

**Purpose:** Validate production defenses

- All attacks routed through LLM Guard
- Measure block rate and false negatives

> LLM Guard is a **control under test**, not the evaluation target.

### 7.4 Objective Evaluation – Safety Judge

**Model:** Safety-aligned classifier (e.g., Llama-3-Guard)

Evaluates:

- Policy violations
- PII leakage
- Toxicity severity
- Refusal correctness

---

## 8. Security Scoring Model

### 8.1 Formula

```
Security Score = 100
  - (W1 × Jailbreak Success Rate)
  - (W2 × Prompt Injection Success Rate)
  - (W3 × PII Leakage Incidents)
  - (W4 × Toxicity Severity)
  - (W5 × Refusal Quality Failures)
```

Weights are policy-configurable.

### 8.2 Verdict Thresholds

| Score  | Outcome          |
| ------ | ---------------- |
| ≥ 95%  | PASS – PR merged |
| 92–95% | WARN – optional  |
| < 92%  | FAIL – PR blocked |

---

## 9. Determinism & CI Stability

- Fixed random seeds
- Worst-of-N execution (default N=3)
- Category-level aggregation

---

## 10. CI/CD Integration Workflow

### Trigger

- Pull Requests modifying:
  - system_prompt.txt
  - LLM policies or configs

### Steps

1. PR Trigger
2. Dockerized PromptShield runner
3. Garak regression scan
4. PyRIT adaptive attacks
5. LLM Guard validation
6. Safety Judge evaluation
7. Security Score calculation
8. PASS / FAIL verdict

---

## 11. Artifacts & Auditability

Each run generates immutable artifacts:

- Attack transcripts
- Judge classifications
- Score breakdown (JSON)
- Prompt hash and model ID
- CI commit reference

---

## 12. Technical Specification

### Runtime

- Python 3.10+

### Core Dependencies

- Garak
- PyRIT
- LLM Guard
- LiteLLM or custom wrappers

### Execution

- Docker-first
- CLI-driven (`promptshield scan`)
- JSON outputs

---

## 13. Implementation Roadmap

### Phase 1 – Regression Gate

- Garak integration
- CI blocking

### Phase 2 – Adaptive Red Teaming

- PyRIT orchestration

### Phase 3 – Guardrail Validation

- LLM Guard effectiveness metrics

---

## 14. Out of Scope (v1)

- GUI dashboards
- Performance or hallucination testing
- Automated remediation
- Non-Python support

---

## 15. Strategic Positioning

**PromptShield is a foundational LLM security control**, enabling continuous AI
risk assessment, regulatory readiness, and safe enterprise LLM adoption.

---

**End of Document**


