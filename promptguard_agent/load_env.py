"""
Helper module to load environment variables from .env file.

This allows the agent to use .env files for configuration.
"""

from __future__ import annotations

import os
from pathlib import Path


def load_env_file(env_path: str | Path | None = None) -> None:
    """
    Load environment variables from a .env file.
    
    Args:
        env_path: Path to .env file. If None, looks for .env in:
                  1. promptguard_agent/.env
                  2. .env (project root)
    """
    if env_path is None:
        # Try promptguard_agent/.env first
        agent_env = Path(__file__).parent / ".env"
        root_env = Path(__file__).parent.parent / ".env"
        
        if agent_env.exists():
            env_path = agent_env
        elif root_env.exists():
            env_path = root_env
        else:
            return  # No .env file found
    
    env_path = Path(env_path)
    if not env_path.exists():
        return
    
    # Simple .env parser (handles KEY=value and # comments)
    with env_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith("#"):
                continue
            
            # Parse KEY=value
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                # Only set if not already in environment
                if key and key not in os.environ:
                    os.environ[key] = value


# Auto-load .env file when this module is imported
load_env_file()

