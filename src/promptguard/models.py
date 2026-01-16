from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class Severity(str, Enum):
    """Security finding severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ProbeType(str, Enum):
    """Types of security probes."""
    SCANNER = "scanner"  # Breadth-first vulnerability discovery
    ATTACK = "attack"  # Goal-driven adversarial testing


@dataclass
class Probe:
    """Represents a single security test probe."""
    probe_id: str
    name: str
    type: ProbeType
    category: str  # e.g., "prompt_injection", "jailbreak", "pii_leakage"
    description: str
    prompt_template: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProbeResult:
    """Result of executing a single probe."""
    probe_id: str
    prompt: str
    response: str
    blocked: bool
    risk_score: float
    severity: Severity
    evidence: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


@dataclass
class AttackNode:
    """Node in an attack graph."""
    node_id: str
    probe_id: str
    condition: Optional[str] = None  # Condition for execution (e.g., "previous.success")
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttackGraph:
    """Directed graph of probes for multi-step attacks."""
    graph_id: str
    name: str
    description: str
    nodes: List[AttackNode]
    edges: List[tuple[str, str]]  # (from_node_id, to_node_id)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AttackGraphResult:
    """Result of executing an attack graph."""
    graph_id: str
    node_results: Dict[str, ProbeResult]  # node_id -> ProbeResult
    overall_risk_score: float
    severity: Severity
    evidence: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Finding:
    """Security finding with explainability."""
    finding_id: str
    probe_id: Optional[str]
    graph_id: Optional[str]
    category: str
    severity: Severity
    risk_score: float
    title: str
    description: str
    evidence: List[str]
    root_cause: str
    remediation: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Policy:
    """Security policy definition."""
    policy_id: str
    name: str
    description: str
    enforcement_mode: str  # "strict" or "advisory"
    failure_conditions: Dict[str, Any]  # Conditions that trigger failures
    severity_thresholds: Dict[str, float]  # Thresholds for each severity
    allowed_models: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PolicyDecision:
    """Decision made by policy enforcement."""
    policy_id: str
    verdict: str  # "PASS", "WARN", "FAIL"
    risk_score: float
    findings: List[Finding]
    explanation: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SecurityReport:
    """Complete security assessment report."""
    report_id: str
    model_id: str
    prompt_hash: Optional[str]
    commit_ref: Optional[str]
    policy_id: str
    decision: PolicyDecision
    probe_results: List[ProbeResult]
    attack_graph_results: List[AttackGraphResult]
    findings: List[Finding]
    metadata: Dict[str, Any] = field(default_factory=dict)
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

