# PromptGuard - ADK-Based LLM Security Framework

PromptGuard is a **policy-driven, automated LLM security framework** designed to prevent prompt injection, jailbreaks, sensitive data leakage, and unsafe model behaviors **before production deployment**. It combines **scanner-based discovery** and **goal-oriented adversarial testing** through a unified, extensible architecture powered by a **Google ADK–based security agent**.

## Architecture

PromptGuard is built around a Google ADK agent that orchestrates security testing:

1. **Probe System**: Security probes (scanner-based and attack-based) test for vulnerabilities
2. **Attack Graphs**: Multi-step adversarial flows for complex attack simulation
3. **Policy Engine**: Policy-as-code enforcement with configurable thresholds
4. **Risk Engine**: Risk scoring and explainability for all findings
5. **Adapter Layer**: Pluggable adapters for legacy tools (Garak, PyRIT, LLM Guard)

## Quick Start

### Installation

```bash
pip install -e .
pip install -e ".[full]"  # Include optional dependencies
```

### Basic Usage

```bash
# Run security assessment
promptguard assess --config promptshield.yaml --policy policy.example.yaml

# Or use the legacy command for backward compatibility
promptshield scan --config promptshield.yaml
```

### Configuration

1. **Config File** (`promptshield.yaml`): Target configuration, guard settings, etc.
2. **Policy File** (`policy.example.yaml`): Security policy with thresholds and enforcement rules
3. **Probes File** (`probes.example.yaml`): Define custom security probes

## Key Components

### Probes

Probes are individual security tests. Two types:

- **Scanner Probes**: Breadth-first vulnerability discovery
- **Attack Probes**: Goal-driven adversarial testing

### Attack Graphs

Attack graphs enable multi-step attacks with conditional execution:

```yaml
graph_id: multi-step-jailbreak
nodes:
  - node_id: step1
    probe_id: initial-probe
  - node_id: step2
    probe_id: follow-up-probe
    condition: previous.success
edges:
  - [step1, step2]
```

### Policy System

Policies define security thresholds and enforcement:

```yaml
policy_id: strict
enforcement_mode: strict
failure_conditions:
  max_critical_findings: 0
  max_risk_score: 5.0
severity_thresholds:
  critical: 3.0
  high: 2.0
```

## ADK Agent

The core of PromptGuard is a Google ADK agent that:

- Interprets policies
- Selects and executes probes
- Runs attack graphs
- Evaluates responses
- Scores risks
- Makes policy-based decisions

The agent is **tool-driven** (not heuristic-driven), ensuring deterministic outcomes.

## Integration with Legacy Code

PromptGuard maintains compatibility with the existing PromptShield codebase:

- Reuses `Target`, `Guard`, and `SafetyJudge` components
- Converts legacy Garak/PyRIT attacks to new Probe format
- Supports existing configuration files

## Output

PromptGuard generates:

- **Security Report** (`security_report.json`): Complete assessment with findings
- **Policy Decision**: PASS/WARN/FAIL verdict with explanation
- **Risk Scores**: Numeric risk scores for all findings
- **Evidence**: Detailed evidence for each finding

## Example

```python
from promptguard.runner import run_security_assessment
from promptshield.config import load_config

config = load_config("promptshield.yaml")
report = run_security_assessment(config, policy_path="policy.example.yaml")

print(f"Verdict: {report.decision.verdict}")
print(f"Risk Score: {report.decision.risk_score}")
print(f"Findings: {len(report.findings)}")
```

## Next Steps

- Add more probe types
- Extend attack graph capabilities
- Integrate with CI/CD pipelines
- Add UI dashboard
- Support for more LLM providers

