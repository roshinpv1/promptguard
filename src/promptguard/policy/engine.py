from __future__ import annotations

from typing import Any, Dict, List

from promptguard.models import Finding, Policy, PolicyDecision, Severity


class PolicyEngine:
    """Engine for policy-as-code enforcement."""

    def evaluate(
        self, policy: Policy, findings: List[Finding], risk_score: float
    ) -> PolicyDecision:
        """
        Evaluate findings against policy and make decision.
        
        Args:
            policy: The policy to enforce
            findings: List of security findings
            risk_score: Overall risk score
        
        Returns:
            PolicyDecision with verdict and explanation
        """
        # Filter findings by severity thresholds
        relevant_findings = self._filter_by_thresholds(policy, findings)
        
        # Check failure conditions
        verdict = self._check_failure_conditions(policy, relevant_findings, risk_score)
        
        # Build explanation
        explanation = self._build_explanation(policy, relevant_findings, verdict)
        
        return PolicyDecision(
            policy_id=policy.policy_id,
            verdict=verdict,
            risk_score=risk_score,
            findings=relevant_findings,
            explanation=explanation,
            metadata={"enforcement_mode": policy.enforcement_mode},
        )
    
    def _filter_by_thresholds(
        self, policy: Policy, findings: List[Finding]
    ) -> List[Finding]:
        """Filter findings based on severity thresholds."""
        filtered = []
        for finding in findings:
            threshold = policy.severity_thresholds.get(finding.severity.value, 0.0)
            if finding.risk_score >= threshold:
                filtered.append(finding)
        return filtered
    
    def _check_failure_conditions(
        self, policy: Policy, findings: List[Finding], risk_score: float
    ) -> str:
        """Check policy failure conditions."""
        conditions = policy.failure_conditions
        
        # Check critical findings
        critical_count = sum(1 for f in findings if f.severity == Severity.CRITICAL)
        if conditions.get("max_critical_findings", 0) > 0:
            if critical_count >= conditions["max_critical_findings"]:
                return "FAIL"
        
        # Check high severity findings
        high_count = sum(1 for f in findings if f.severity == Severity.HIGH)
        if conditions.get("max_high_findings", 0) > 0:
            if high_count >= conditions["max_high_findings"]:
                return "FAIL"
        
        # Check risk score threshold
        risk_threshold = conditions.get("max_risk_score", 100.0)
        if risk_score >= risk_threshold:
            return "FAIL"
        
        # Check warning threshold
        warn_threshold = conditions.get("warn_risk_score", risk_threshold * 0.9)
        if risk_score >= warn_threshold:
            return "WARN"
        
        return "PASS"
    
    def _build_explanation(
        self, policy: Policy, findings: List[Finding], verdict: str
    ) -> str:
        """Build human-readable explanation."""
        parts = [f"Policy: {policy.name}"]
        parts.append(f"Verdict: {verdict}")
        
        if findings:
            parts.append(f"Findings: {len(findings)}")
            for finding in findings[:5]:  # Top 5
                parts.append(f"  - {finding.title} ({finding.severity.value})")
        else:
            parts.append("No findings above thresholds")
        
        return "\n".join(parts)

