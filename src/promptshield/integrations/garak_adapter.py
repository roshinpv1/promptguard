from __future__ import annotations

from importlib import import_module
from typing import List, Optional

from promptshield.models import Attack


def build_garak_attacks_from_library(probes: List[str]) -> List[Attack]:
    try:
        import_module("garak")
    except ImportError as exc:
        raise RuntimeError("garak is not installed.") from exc

    attacks: List[Attack] = []
    attack_id = 0
    for probe in probes:
        prompts = _probe_to_prompts(probe)
        for prompt in prompts:
            attacks.append(
                Attack(
                    attack_id=f"garak-{attack_id:03d}",
                    category="prompt_injection",
                    prompt=prompt,
                    source="garak",
                )
            )
            attack_id += 1
    return attacks


def _probe_to_prompts(probe: str) -> List[str]:
    probe_cls = _resolve_probe_class(probe)
    if not probe_cls:
        return [probe]

    instance = probe_cls()
    if hasattr(instance, "prompts"):
        prompts = instance.prompts
        if callable(prompts):
            return list(prompts())
        if isinstance(prompts, list):
            return prompts
    if hasattr(instance, "prompt") and isinstance(instance.prompt, str):
        return [instance.prompt]
    return [probe]


def _resolve_probe_class(path: str) -> Optional[type]:
    if ":" in path:
        module_path, class_name = path.split(":", 1)
    elif "." in path:
        parts = path.split(".")
        module_path = ".".join(parts[:-1])
        class_name = parts[-1]
    else:
        return None

    try:
        module = import_module(module_path)
    except ImportError:
        return None
    return getattr(module, class_name, None)

