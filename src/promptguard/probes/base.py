from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from promptguard.models import Probe, ProbeResult


class ProbeExecutor(ABC):
    """Base class for executing security probes."""

    @abstractmethod
    def execute(self, probe: Probe, context: Dict[str, Any]) -> ProbeResult:
        """
        Execute a probe and return the result.
        
        Args:
            probe: The probe to execute
            context: Execution context (target, guard, system_prompt, etc.)
        
        Returns:
            ProbeResult with findings
        """
        raise NotImplementedError


class ProbeGenerator(ABC):
    """Base class for generating probe prompts."""

    @abstractmethod
    def generate(self, probe: Probe, context: Dict[str, Any]) -> str:
        """
        Generate the attack prompt for a probe.
        
        Args:
            probe: The probe definition
            context: Context for generation
        
        Returns:
            Generated prompt string
        """
        raise NotImplementedError

