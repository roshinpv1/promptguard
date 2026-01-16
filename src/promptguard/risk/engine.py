from __future__ import annotations

from typing import List

from promptguard.models import Finding, ProbeResult, Severity


class RiskEngine:
    """Engine for risk scoring and explainability."""

    def compute_risk_score(self, results: List[ProbeResult]) -> float:
        """Compute overall risk score from probe results."""
        if not results:
            return 0.0
        
        # Weighted sum based on severity
        weights = {
            Severity.CRITICAL: 4.0,
            Severity.HIGH: 3.0,
            Severity.MEDIUM: 2.0,
            Severity.LOW: 1.0,
            Severity.INFO: 0.0,
        }
        
        total_weighted = sum(
            weights.get(result.severity, 0.0) * result.risk_score for result in results
        )
        total_weight = sum(weights.get(result.severity, 0.0) for result in results)
        
        if total_weight == 0:
            return 0.0
        
        return total_weighted / total_weight
    
    def generate_findings(
        self, probe_results: List[ProbeResult], attack_graph_results: List[Any]
    ) -> List[Finding]:
        """Generate findings from probe and attack graph results."""
        findings = []
        
        # Findings from probe results
        for result in probe_results:
            if result.risk_score > 0:
                finding = Finding(
                    finding_id=f"finding-{result.probe_id}",
                    probe_id=result.probe_id,
                    graph_id=None,
                    category=result.metadata.get("category", "unknown"),
                    severity=result.severity,
                    risk_score=result.risk_score,
                    title=f"Security issue in {result.probe_id}",
                    description=f"Probe {result.probe_id} detected a security issue.",
                    evidence=result.evidence,
                    root_cause=self._infer_root_cause(result),
                    remediation=self._suggest_remediation(result),
                    metadata=result.metadata,
                )
                findings.append(finding)
        
        # Findings from attack graph results
        for graph_result in attack_graph_results:
            if graph_result.overall_risk_score > 0:
                finding = Finding(
                    finding_id=f"finding-{graph_result.graph_id}",
                    probe_id=None,
                    graph_id=graph_result.graph_id,
                    category="multi_step_attack",
                    severity=graph_result.severity,
                    risk_score=graph_result.overall_risk_score,
                    title=f"Multi-step attack successful: {graph_result.graph_id}",
                    description=f"Attack graph {graph_result.graph_id} successfully bypassed defenses.",
                    evidence=graph_result.evidence,
                    root_cause="Multi-step attack sequence bypassed individual defenses",
                    remediation="Implement multi-turn conversation monitoring and stateful guardrails",
                    metadata=graph_result.metadata,
                )
                findings.append(finding)
        
        return findings
    
    def _infer_root_cause(self, result: ProbeResult) -> str:
        """Infer root cause from probe result."""
        if result.blocked:
            return "Guardrail blocked the attack, but may need tuning"
        
        category = result.metadata.get("category", "unknown")
        if category == "prompt_injection":
            return "System prompt vulnerable to injection attacks"
        elif category == "jailbreak":
            return "Model safety guardrails can be bypassed"
        elif category == "pii_leakage":
            return "Model may leak sensitive information"
        else:
            return "Security vulnerability detected"
    
    def _suggest_remediation(self, result: ProbeResult) -> str:
        """Suggest remediation based on probe result."""
        category = result.metadata.get("category", "unknown")
        if category == "prompt_injection":
            return "Add input sanitization and prompt injection detection"
        elif category == "jailbreak":
            return "Strengthen system prompt and add refusal training"
        elif category == "pii_leakage":
            return "Implement output filtering and PII detection"
        else:
            return "Review and strengthen security controls"

