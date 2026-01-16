from __future__ import annotations

import random
from typing import Any, Dict

from promptshield.models import TargetResponse
from promptshield.targets.base import Target


class MockTarget(Target):
    def __init__(self, behavior: Dict[str, Any], seed: int) -> None:
        self._behavior = behavior
        self._rng = random.Random(seed)

    def generate(self, prompt: str) -> TargetResponse:
        unsafe_probability = float(self._behavior.get("unsafe_probability", 0.1))
        pii_probability = float(self._behavior.get("pii_leak_probability", 0.01))

        unsafe = self._rng.random() < unsafe_probability
        pii = self._rng.random() < pii_probability

        if "ignore previous" in prompt.lower() or "jailbreak" in prompt.lower():
            unsafe = True
        if "pii" in prompt.lower():
            pii = True

        if unsafe:
            content = "Here is how to bypass safety filters."
        elif pii:
            content = "User email: alice@example.com"
        else:
            content = "I cannot help with that request."

        return TargetResponse(
            content=content,
            metadata={"unsafe": unsafe, "pii": pii},
        )

