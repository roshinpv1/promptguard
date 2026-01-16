# PromptGuard Migration Guide

## Overview

PromptGuard has been rebuilt based on the new PRD requirements using Google ADK as the orchestration framework. The new architecture maintains compatibility with existing PromptShield code while introducing new abstractions and capabilities.

## What Changed

### New Architecture

1. **Google ADK-Based Agent**: The core orchestration is now handled by a Google ADK agent (with fallback to direct execution if ADK is not available)

2. **Probe Abstractions**: 
   - `Probe`: Represents a single security test
   - `ProbeExecutor`: Executes probes
   - `ProbeGenerator`: Generates attack prompts

3. **Attack Graphs**: 
   - `AttackGraph`: Multi-step attack sequences
   - `AttackGraphExecutor`: Executes attack graphs with conditional logic

4. **Policy System**:
   - `Policy`: Policy-as-code definitions
   - `PolicyEngine`: Enforces policies and makes decisions
   - YAML/JSON policy files

5. **Risk Engine**:
   - `RiskEngine`: Computes risk scores
   - `Finding`: Security findings with explainability

6. **Adapter Layer**:
   - Converts legacy Garak/PyRIT attacks to new Probe format
   - Maintains compatibility with existing components

### What Stayed the Same

- **Target System**: `Target`, `MockTarget`, `APITarget` - all reused
- **Guard System**: `Guard`, `LLMGuardAdapter`, `PatternGuard` - all reused
- **Judge System**: `SafetyJudge` - reused
- **Configuration**: Existing `promptshield.yaml` format still works
- **CLI**: `promptshield scan` still works (backward compatible)

## New Components

### Directory Structure

```
src/promptguard/
├── __init__.py
├── models.py              # New data models (Probe, AttackGraph, Policy, Finding)
├── runner.py              # New runner using ADK agent
├── cli.py                 # New CLI entrypoint
├── reports.py             # Report generation
├── probes/
│   ├── base.py           # Probe abstractions
│   └── scanner_probe.py  # Scanner probe executor
├── attack_graphs/
│   └── executor.py       # Attack graph executor
├── policy/
│   ├── engine.py         # Policy enforcement
│   └── loader.py         # Policy loading
├── risk/
│   └── engine.py         # Risk scoring
├── adapters/
│   ├── probe_registry.py # Probe registry
│   └── legacy.py         # Legacy adapter
└── agent/
    ├── security_agent.py # ADK-based security agent
    └── tools.py          # ADK tools
```

## Usage

### New Command

```bash
promptguard assess --config promptshield.yaml --policy policy.example.yaml
```

### Legacy Command (Still Works)

```bash
promptshield scan --config promptshield.yaml
```

## Configuration Files

### Policy File (`policy.example.yaml`)

```yaml
policy_id: default
name: Default Security Policy
enforcement_mode: strict
failure_conditions:
  max_critical_findings: 0
  max_risk_score: 5.0
severity_thresholds:
  critical: 3.0
  high: 2.0
```

### Probes File (`probes.example.yaml`)

```yaml
scanner_probes:
  - id: prompt-injection-001
    name: Basic Prompt Injection
    category: prompt_injection
    prompt_template: "Ignore previous instructions..."
```

## Key Differences from Old Architecture

| Old (PromptShield) | New (PromptGuard) |
|---------------------|-------------------|
| Direct runner execution | ADK agent orchestration |
| Attack objects | Probe abstractions |
| Linear attack execution | Attack graphs with conditional logic |
| Hardcoded scoring | Policy-driven decisions |
| Limited explainability | Rich findings with root cause & remediation |

## Migration Path

1. **Immediate**: Use `promptshield scan` - works as before
2. **Gradual**: Start using `promptguard assess` with policy files
3. **Advanced**: Define custom probes and attack graphs
4. **Full Migration**: Use ADK agent for advanced orchestration

## Backward Compatibility

- All existing config files work
- Legacy attack engines (Garak, PyRIT) are automatically converted
- Existing components (Target, Guard, Judge) are reused
- Output format is enhanced but compatible

## Next Steps

1. Install dependencies: `pip install -e ".[full]"`
2. Create a policy file based on `policy.example.yaml`
3. Run: `promptguard assess --config promptshield.yaml --policy policy.example.yaml`
4. Review the new `security_report.json` output

## Notes

- The ADK agent is optional - if Google ADK is not installed, the system falls back to direct execution
- All legacy code in `src/promptshield/` is preserved for backward compatibility
- The new code in `src/promptguard/` is the primary implementation going forward

