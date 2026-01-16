from __future__ import annotations

from typing import Any, Dict

from promptguard.adapters.legacy import LegacyAdapter
from promptguard.attack_graphs.executor import AttackGraphExecutor
from promptguard.models import AttackGraph, Probe, ProbeResult
from promptguard.probes.base import ProbeExecutor
from promptguard.probes.scanner_probe import ScannerProbeExecutor


def execute_probe_tool(
    probe_id: str,
    probe_registry: Dict[str, Probe] | None = None,
    context: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    ADK tool for executing a single security probe.
    
    Args:
        probe_id: ID of the probe to execute
        probe_registry: Registry of available probes
        context: Execution context (target, guard, evaluator, etc.)
    
    Returns:
        Dictionary with probe result
    """
    if not probe_registry:
        return {"error": "Probe registry not provided"}
    if not context:
        return {"error": "Context not provided"}
    
    probe = probe_registry.get(probe_id)
    if not probe:
        return {"error": f"Probe {probe_id} not found"}
    
    executor: ProbeExecutor = ScannerProbeExecutor()
    result = executor.execute(probe, context)
    
    return {
        "probe_id": result.probe_id,
        "risk_score": result.risk_score,
        "severity": result.severity.value,
        "blocked": result.blocked,
        "evidence": result.evidence,
        "success": result.risk_score > 0,
    }


def execute_attack_graph_tool(
    graph_id: str,
    graph: AttackGraph,
    probe_registry: Dict[str, Probe] | None = None,
    context: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    ADK tool for executing an attack graph.
    
    Args:
        graph_id: ID of the attack graph
        graph: The attack graph to execute
        probe_registry: Registry of available probes
        context: Execution context
    
    Returns:
        Dictionary with attack graph result
    """
    if not probe_registry:
        return {"error": "Probe registry not provided"}
    if not context:
        return {"error": "Context not provided"}
    
    executor = AttackGraphExecutor(
        probe_executor=ScannerProbeExecutor(),
        probe_registry=probe_registry,
    )
    
    result = executor.execute(graph, context)
    
    return {
        "graph_id": result.graph_id,
        "overall_risk_score": result.overall_risk_score,
        "severity": result.severity.value,
        "node_results": {
            node_id: {
                "risk_score": probe_result.risk_score,
                "severity": probe_result.severity.value,
            }
            for node_id, probe_result in result.node_results.items()
        },
        "evidence": result.evidence,
        "success": result.overall_risk_score > 0,
    }


def evaluate_response_tool(
    probe: Probe,
    response: str,
    evaluator: Any,
) -> Dict[str, Any]:
    """
    ADK tool for evaluating a model response.
    
    Args:
        probe: The probe that generated the attack
        response: The model's response
        evaluator: Response evaluator (e.g., SafetyJudge)
    
    Returns:
        Dictionary with evaluation result
    """
    from promptshield.models import Attack, TargetResponse
    
    # Convert to legacy format for evaluation
    attack = Attack(
        attack_id=probe.probe_id,
        category=probe.category,
        prompt=probe.prompt_template,
        source="adk",
    )
    
    target_response = TargetResponse(content=response, blocked=False)
    
    evaluation = evaluator.evaluate(attack, target_response)
    
    return {
        "risk_score": evaluation.risk_score(),
        "jailbreak_success": evaluation.jailbreak_success,
        "prompt_injection_success": evaluation.prompt_injection_success,
        "pii_leak": evaluation.pii_leak,
        "toxicity_severity": evaluation.toxicity_severity,
        "refusal_quality_failure": evaluation.refusal_quality_failure,
        "notes": evaluation.notes,
    }

