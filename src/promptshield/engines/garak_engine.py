from __future__ import annotations

from typing import List

from promptshield.models import Attack
from promptshield.integrations.garak_adapter import build_garak_attacks_from_library


def build_garak_attacks(probes: List[str], use_library: bool = False) -> List[Attack]:
    if use_library:
        return build_garak_attacks_from_library(probes)
    attacks: List[Attack] = []
    for idx, probe in enumerate(probes):
        attacks.append(
            Attack(
                attack_id=f"garak-{idx:03d}",
                category="prompt_injection",
                prompt=probe,
                source="garak",
            )
        )
    return attacks

