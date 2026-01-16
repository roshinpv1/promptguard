from __future__ import annotations

import re
from typing import List

from promptshield.guard.base import Guard
from promptshield.models import GuardDecision, TargetResponse


class PatternGuard(Guard):
    def __init__(self, block_on_patterns: List[str]) -> None:
        self._patterns = [re.compile(p, re.IGNORECASE) for p in block_on_patterns]

    def scan_input(self, prompt: str) -> GuardDecision:
        for pattern in self._patterns:
            if pattern.search(prompt):
                return GuardDecision(
                    prompt=prompt,
                    blocked=True,
                    reason="Blocked by pattern guard (input).",
                    metadata={"guard_blocked": True},
                )
        return GuardDecision(
            prompt=prompt,
            blocked=False,
            metadata={"guard_blocked": False},
        )

    def scan_output(self, prompt: str, response: TargetResponse) -> TargetResponse:
        for pattern in self._patterns:
            if pattern.search(response.content):
                return TargetResponse(
                    content="Request blocked by guardrail.",
                    blocked=True,
                    metadata={**response.metadata, "guard_blocked": True},
                )
        return TargetResponse(
            content=response.content,
            blocked=False,
            metadata={**response.metadata, "guard_blocked": False},
        )

