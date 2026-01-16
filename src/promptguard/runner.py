from __future__ import annotations

from typing import Any, Dict

from promptguard.adapters.legacy import LegacyAdapter
from promptguard.adapters.probe_registry import ProbeRegistry
from promptguard.agent.security_agent import PromptGuardSecurityAgent
from promptguard.models import Policy, SecurityReport
from promptguard.policy.loader import load_policy
from promptshield.config import PromptShieldConfig
from promptshield.guard.base import Guard
from promptshield.judge.safety_judge import SafetyJudge
from promptshield.targets.base import Target
from promptshield.targets.mock import MockTarget
from promptshield.utils import current_commit_ref, sha256_file


def _load_target(config: PromptShieldConfig) -> Target:
    """Load target from config."""
    if config.target.type == "api":
        from promptshield.targets.api_target import APITarget
        return APITarget(
            api_url=config.target.api_url or "",
            model_id=config.target.model_id,
            api_key=config.target.api_key,
            api_type=config.target.api_type,
            headers=config.target.headers,
        )
    return MockTarget(config.target.behavior, seed=config.run.seed)


def _load_guard(config: PromptShieldConfig) -> Guard | None:
    """Load guard from config."""
    if not config.guard.enabled:
        return None
    if config.guard.type == "llm_guard":
        from promptshield.integrations.llm_guard_adapter import LLMGuardAdapter
        try:
            return LLMGuardAdapter(
                input_scanners=config.guard.input_scanners,
                output_scanners=config.guard.output_scanners,
            )
        except ImportError:
            from promptshield.guard.llm_guard import PatternGuard
            return PatternGuard(config.guard.block_on_patterns)
    from promptshield.guard.llm_guard import PatternGuard
    return PatternGuard(config.guard.block_on_patterns)


def run_security_assessment(
    config: PromptShieldConfig,
    policy_path: str | None = None,
) -> SecurityReport:
    """
    Run a security assessment using the ADK-based agent.
    
    Args:
        config: PromptShield configuration
        policy_path: Path to policy YAML file (optional)
    
    Returns:
        SecurityReport with findings and decision
    """
    # Load policy
    if policy_path:
        policy = load_policy(policy_path)
    else:
        # Create default policy from config
        from promptguard.models import Policy
        policy = Policy(
            policy_id="default",
            name="Default Policy",
            description="Default security policy",
            enforcement_mode="strict",
            failure_conditions={
                "max_risk_score": 100.0 - config.scoring.thresholds.get("pass", 95),
                "warn_risk_score": 100.0 - config.scoring.thresholds.get("warn", 92),
            },
            severity_thresholds={},
        )
    
    # Load components
    target = _load_target(config)
    guard = _load_guard(config)
    evaluator = SafetyJudge(config.judge.toxicity_terms)
    
    # Build probe registry
    registry = ProbeRegistry()
    
    # Convert legacy probes to new format
    adapter = LegacyAdapter()
    if config.attacks.garak:
        garak_probes = config.attacks.garak.get("probes", [])
        for probe in adapter.convert_garak_probes(garak_probes):
            registry.register(probe)
    
    if config.attacks.pyrit:
        pyrit_prompts = config.attacks.pyrit.get("base_prompts", [])
        pyrit_mutations = config.attacks.pyrit.get("mutations", [])
        for probe in adapter.convert_pyrit_probes(pyrit_prompts, pyrit_mutations):
            registry.register(probe)
    
    # Create agent
    agent = PromptGuardSecurityAgent(
        model="gemini-3-flash-preview",
        probe_registry=registry._probes,
        policy=policy,
    )
    
    # Run assessment
    system_prompt_path = config.run.prompt_path
    system_prompt = ""
    if system_prompt_path:
        from pathlib import Path
        system_prompt = Path(system_prompt_path).read_text()
    
    report = agent.run_security_assessment(
        target=target,
        guard=guard,
        system_prompt=system_prompt,
        evaluator=evaluator,
        scanner_probes=registry.get_all_scanner_probes(),
        attack_graphs=[],  # Can be added from config
    )
    
    # Update report metadata
    report.prompt_hash = sha256_file(system_prompt_path) if system_prompt_path else None
    report.commit_ref = current_commit_ref()
    report.model_id = config.target.model_id
    
    return report

