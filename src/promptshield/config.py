from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


@dataclass
class RunConfig:
    seed: int = 1337
    worst_of_n: int = 3
    output_dir: str = "artifacts"
    prompt_path: Optional[str] = None


@dataclass
class TargetConfig:
    type: str = "mock"
    model_id: str = "mock-llm"
    behavior: Dict[str, Any] = field(default_factory=dict)
    api_url: Optional[str] = None
    api_key: Optional[str] = None
    api_type: str = "openai"
    headers: Optional[Dict[str, str]] = None


@dataclass
class GuardConfig:
    enabled: bool = True
    type: str = "pattern"
    block_on_patterns: List[str] = field(default_factory=list)
    input_scanners: List[str] = field(default_factory=list)
    output_scanners: List[str] = field(default_factory=list)


@dataclass
class JudgeConfig:
    type: str = "heuristic"
    toxicity_terms: List[str] = field(default_factory=list)


@dataclass
class ScoringConfig:
    weights: Dict[str, float] = field(default_factory=dict)
    thresholds: Dict[str, float] = field(default_factory=dict)


@dataclass
class AttackConfig:
    garak: Dict[str, Any] = field(default_factory=dict)
    pyrit: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PromptShieldConfig:
    version: int
    run: RunConfig
    target: TargetConfig
    guard: GuardConfig
    judge: JudgeConfig
    scoring: ScoringConfig
    attacks: AttackConfig


def _read_yaml(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_config(path: str) -> PromptShieldConfig:
    data = _read_yaml(Path(path))

    run = RunConfig(**data.get("run", {}))
    target = TargetConfig(**data.get("target", {}))
    guard = GuardConfig(**data.get("guard", {}))
    judge = JudgeConfig(**data.get("judge", {}))
    scoring = ScoringConfig(**data.get("scoring", {}))
    attacks = AttackConfig(**data.get("attacks", {}))

    return PromptShieldConfig(
        version=data.get("version", 1),
        run=run,
        target=target,
        guard=guard,
        judge=judge,
        scoring=scoring,
        attacks=attacks,
    )

