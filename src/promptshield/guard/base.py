from __future__ import annotations

from abc import ABC, abstractmethod

from promptshield.models import GuardDecision, TargetResponse


class Guard(ABC):
    @abstractmethod
    def scan_input(self, prompt: str) -> GuardDecision:
        raise NotImplementedError

    @abstractmethod
    def scan_output(self, prompt: str, response: TargetResponse) -> TargetResponse:
        raise NotImplementedError

