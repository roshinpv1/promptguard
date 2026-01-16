from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Attack:
    attack_id: str
    category: str
    prompt: str
    source: str


@dataclass
class TargetResponse:
    content: str
    blocked: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GuardDecision:
    prompt: str
    blocked: bool
    reason: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JudgeResult:
    jailbreak_success: bool
    prompt_injection_success: bool
    pii_leak: bool
    toxicity_severity: float
    refusal_quality_failure: bool
    notes: List[str] = field(default_factory=list)

    def risk_score(self) -> float:
        score = 0.0
        if self.jailbreak_success:
            score += 1.0
        if self.prompt_injection_success:
            score += 1.0
        if self.pii_leak:
            score += 1.0
        score += self.toxicity_severity
        if self.refusal_quality_failure:
            score += 1.0
        return score


@dataclass
class AttackResult:
    attack: Attack
    response: TargetResponse
    judge: JudgeResult
    attempts: int
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


@dataclass
class ScoreBreakdown:
    security_score: float
    jailbreak_success_rate: float
    prompt_injection_success_rate: float
    pii_leak_rate: float
    toxicity_severity: float
    refusal_quality_fail_rate: float
    guard_block_rate: float
    guard_false_negative_rate: float
    verdict: str
    thresholds: Dict[str, float]


@dataclass
class RunArtifacts:
    run_id: str
    model_id: str
    prompt_hash: Optional[str]
    commit_ref: Optional[str]
    results: List[AttackResult]
    score: ScoreBreakdown
    metadata: Dict[str, Any] = field(default_factory=dict)

