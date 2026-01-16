from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path
from typing import Dict, Any

from promptshield.config import PromptShieldConfig, load_config
from promptshield.runner import run_scan
from promptshield.models import RunArtifacts


async def run_scan_async(config_dict: Dict[str, Any], system_prompt: str | None = None) -> RunArtifacts:
    """
    Run a PromptShield scan asynchronously.
    
    Args:
        config_dict: Configuration dictionary
        system_prompt: Optional system prompt content (creates temp file if provided)
    
    Returns:
        RunArtifacts from the scan
    """
    # Create temp system prompt file if provided
    prompt_path = None
    if system_prompt:
        # Create temp system prompt file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(system_prompt)
            prompt_path = f.name
        
        # Update config with prompt path
        if "run" not in config_dict:
            config_dict["run"] = {}
        config_dict["run"]["prompt_path"] = prompt_path
    
    # Create config from dict
    from promptshield.config import (
        RunConfig, TargetConfig, GuardConfig, JudgeConfig,
        ScoringConfig, AttackConfig, PromptShieldConfig
    )
    config = PromptShieldConfig(
        version=config_dict.get("version", 1),
        run=RunConfig(**config_dict.get("run", {})),
        target=TargetConfig(**config_dict.get("target", {})),
        guard=GuardConfig(**config_dict.get("guard", {})),
        judge=JudgeConfig(**config_dict.get("judge", {})),
        scoring=ScoringConfig(**config_dict.get("scoring", {})),
        attacks=AttackConfig(**config_dict.get("attacks", {})),
    )
    
    # Run in executor to avoid blocking
    loop = asyncio.get_event_loop()
    artifacts = await loop.run_in_executor(None, run_scan, config)
    
    # Clean up temp prompt file after scan
    if prompt_path and Path(prompt_path).exists():
        Path(prompt_path).unlink(missing_ok=True)
    
    return artifacts

