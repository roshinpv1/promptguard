from __future__ import annotations

from typing import Any, Dict, List

from promptguard.models import Probe, ProbeType
from promptguard.probes.base import ProbeExecutor
from promptguard.probes.scanner_probe import ScannerProbeExecutor

# Import legacy components that can be reused
from promptshield.judge.safety_judge import SafetyJudge
from promptshield.targets.base import Target
from promptshield.guard.base import Guard


class LegacyAdapter:
    """Adapter to convert legacy attack engines to new probe system."""

    @staticmethod
    def convert_garak_probes(probes: List[str]) -> List[Probe]:
        """Convert Garak-style probes to new Probe model."""
        result = []
        for idx, prompt in enumerate(probes):
            probe = Probe(
                probe_id=f"garak-{idx:03d}",
                name=f"Garak Probe {idx}",
                type=ProbeType.SCANNER,
                category="prompt_injection",
                description="Garak-style prompt injection probe",
                prompt_template=prompt,
                metadata={"source": "garak", "legacy": True},
            )
            result.append(probe)
        return result

    @staticmethod
    def convert_pyrit_probes(base_prompts: List[str], mutations: List[str]) -> List[Probe]:
        """Convert PyRIT-style probes to new Probe model."""
        result = []
        for idx, prompt in enumerate(base_prompts):
            probe = Probe(
                probe_id=f"pyrit-{idx:03d}",
                name=f"PyRIT Probe {idx}",
                type=ProbeType.ATTACK,
                category="jailbreak",
                description="PyRIT-style adaptive attack probe",
                prompt_template=prompt,
                metadata={"source": "pyrit", "mutations": mutations, "legacy": True},
            )
            result.append(probe)
        return result

    @staticmethod
    def create_executor_context(
        target: Target, guard: Guard | None, system_prompt: str, evaluator: Any
    ) -> Dict[str, Any]:
        """Create execution context from legacy components."""
        return {
            "target": target,
            "guard": guard,
            "system_prompt": system_prompt,
            "evaluator": evaluator,
        }

