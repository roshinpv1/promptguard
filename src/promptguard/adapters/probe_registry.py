from __future__ import annotations

from typing import Any, Dict, List

from promptguard.models import Probe, ProbeType


class ProbeRegistry:
    """Registry for security probes."""

    def __init__(self):
        self._probes: Dict[str, Probe] = {}
        self._scanner_probes: List[Probe] = []
        self._attack_probes: List[Probe] = []

    def register(self, probe: Probe) -> None:
        """Register a probe."""
        self._probes[probe.probe_id] = probe
        if probe.type == ProbeType.SCANNER:
            self._scanner_probes.append(probe)
        elif probe.type == ProbeType.ATTACK:
            self._attack_probes.append(probe)

    def get(self, probe_id: str) -> Probe | None:
        """Get a probe by ID."""
        return self._probes.get(probe_id)

    def get_all_scanner_probes(self) -> List[Probe]:
        """Get all scanner probes."""
        return self._scanner_probes.copy()

    def get_all_attack_probes(self) -> List[Probe]:
        """Get all attack probes."""
        return self._attack_probes.copy()

    def load_from_config(self, config: Dict[str, Any]) -> None:
        """Load probes from configuration."""
        # Load scanner probes
        scanner_configs = config.get("scanner_probes", [])
        for idx, probe_config in enumerate(scanner_configs):
            probe = Probe(
                probe_id=probe_config.get("id", f"scanner-{idx:03d}"),
                name=probe_config.get("name", f"Scanner Probe {idx}"),
                type=ProbeType.SCANNER,
                category=probe_config.get("category", "unknown"),
                description=probe_config.get("description", ""),
                prompt_template=probe_config.get("prompt_template", ""),
                metadata=probe_config.get("metadata", {}),
            )
            self.register(probe)
        
        # Load attack probes
        attack_configs = config.get("attack_probes", [])
        for idx, probe_config in enumerate(attack_configs):
            probe = Probe(
                probe_id=probe_config.get("id", f"attack-{idx:03d}"),
                name=probe_config.get("name", f"Attack Probe {idx}"),
                type=ProbeType.ATTACK,
                category=probe_config.get("category", "unknown"),
                description=probe_config.get("description", ""),
                prompt_template=probe_config.get("prompt_template", ""),
                metadata=probe_config.get("metadata", {}),
            )
            self.register(probe)

