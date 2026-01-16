from __future__ import annotations

from importlib import import_module
from typing import Callable, List, Optional

from promptshield.models import Attack


def build_pyrit_attacks_from_library(
    base_prompts: List[str],
    mutations: List[str],
    generator_path: Optional[str],
) -> List[Attack]:
    try:
        import_module("pyrit")
    except ImportError as exc:
        raise RuntimeError("pyrit is not installed.") from exc

    if not generator_path:
        raise RuntimeError("pyrit generator path is required for library integration.")

    generator = _load_callable(generator_path)
    prompts = generator(base_prompts, mutations)
    if not isinstance(prompts, list):
        raise RuntimeError("pyrit generator must return a list of prompts.")

    attacks: List[Attack] = []
    for idx, prompt in enumerate(prompts):
        attacks.append(
            Attack(
                attack_id=f"pyrit-{idx:03d}",
                category="jailbreak",
                prompt=str(prompt),
                source="pyrit",
            )
        )
    return attacks


def _load_callable(path: str) -> Callable[..., List[str]]:
    if ":" in path:
        module_path, func_name = path.split(":", 1)
    else:
        parts = path.split(".")
        module_path = ".".join(parts[:-1])
        func_name = parts[-1]
    module = import_module(module_path)
    func = getattr(module, func_name, None)
    if not callable(func):
        raise RuntimeError(f"pyrit generator callable not found: {path}")
    return func

