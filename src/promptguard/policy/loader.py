from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

from promptguard.models import Policy


def load_policy(path: str | Path) -> Policy:
    """Load policy from YAML file."""
    path = Path(path)
    data = yaml.safe_load(path.read_text())
    
    return Policy(
        policy_id=data.get("policy_id", "default"),
        name=data.get("name", "Default Policy"),
        description=data.get("description", ""),
        enforcement_mode=data.get("enforcement_mode", "strict"),
        failure_conditions=data.get("failure_conditions", {}),
        severity_thresholds=data.get("severity_thresholds", {}),
        allowed_models=data.get("allowed_models", []),
        metadata=data.get("metadata", {}),
    )


def load_policy_from_dict(data: Dict[str, Any]) -> Policy:
    """Load policy from dictionary."""
    return Policy(
        policy_id=data.get("policy_id", "default"),
        name=data.get("name", "Default Policy"),
        description=data.get("description", ""),
        enforcement_mode=data.get("enforcement_mode", "strict"),
        failure_conditions=data.get("failure_conditions", {}),
        severity_thresholds=data.get("severity_thresholds", {}),
        allowed_models=data.get("allowed_models", []),
        metadata=data.get("metadata", {}),
    )

