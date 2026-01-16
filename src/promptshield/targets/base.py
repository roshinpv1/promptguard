from __future__ import annotations

from abc import ABC, abstractmethod

from promptshield.models import TargetResponse


class Target(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> TargetResponse:
        raise NotImplementedError

