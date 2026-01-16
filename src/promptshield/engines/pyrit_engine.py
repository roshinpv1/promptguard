from __future__ import annotations

from typing import List, Optional

from promptshield.models import Attack
from promptshield.integrations.pyrit_adapter import build_pyrit_attacks_from_library


def _mutate(prompt: str, mutation: str) -> str:
    if mutation == "obfuscate":
        return f"[[{prompt}]] (base64: {prompt.encode().hex()})"
    if mutation == "social_engineering":
        return f"Compliance audit: {prompt} Please respond fully."
    return prompt


def build_pyrit_attacks(
    base_prompts: List[str],
    mutations: List[str],
    use_library: bool = False,
    generator_path: Optional[str] = None,
) -> List[Attack]:
    if use_library:
        return build_pyrit_attacks_from_library(base_prompts, mutations, generator_path)
    attacks: List[Attack] = []
    attack_id = 0
    for prompt in base_prompts:
        if not mutations:
            attacks.append(
                Attack(
                    attack_id=f"pyrit-{attack_id:03d}",
                    category="jailbreak",
                    prompt=prompt,
                    source="pyrit",
                )
            )
            attack_id += 1
            continue
        for mutation in mutations:
            attacks.append(
                Attack(
                    attack_id=f"pyrit-{attack_id:03d}",
                    category="jailbreak",
                    prompt=_mutate(prompt, mutation),
                    source="pyrit",
                )
            )
            attack_id += 1
    return attacks

