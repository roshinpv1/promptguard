from __future__ import annotations

from importlib import import_module
from typing import Any, Iterable, List, Tuple

from promptshield.guard.base import Guard
from promptshield.models import GuardDecision, TargetResponse


class LLMGuardAdapter(Guard):
    """LLM Guard adapter - requires llm-guard package to be installed."""
    
    def __init__(self, input_scanners: List[str], output_scanners: List[str]):
        if not _check_llm_guard_installed():
            raise ImportError(
                "llm-guard is not installed. Install it with: pip install llm-guard\n"
                "Note: llm-guard may not support Python 3.13. Use Python 3.10-3.12 for full support."
            )
    def __init__(self, input_scanners: List[str], output_scanners: List[str]) -> None:
        self._scan_prompt, self._scan_output = _load_llm_guard_scan_functions()
        self._input_scanners = _build_scanners("llm_guard.input_scanners", input_scanners)
        self._output_scanners = _build_scanners("llm_guard.output_scanners", output_scanners)

    def scan_input(self, prompt: str) -> GuardDecision:
        if not self._input_scanners:
            return GuardDecision(prompt=prompt, blocked=False)
        sanitized, is_valid, risk_score, details = _scan_prompt(
            self._scan_prompt, self._input_scanners, prompt
        )
        return GuardDecision(
            prompt=sanitized,
            blocked=not is_valid,
            reason=None if is_valid else "Blocked by LLM Guard input scan.",
            metadata={"llm_guard_input_risk": risk_score, "llm_guard_input": details},
        )

    def scan_output(self, prompt: str, response: TargetResponse) -> TargetResponse:
        if not self._output_scanners:
            return response
        sanitized, is_valid, risk_score, details = _scan_output(
            self._scan_output, self._output_scanners, prompt, response.content
        )
        if not is_valid:
            return TargetResponse(
                content="Request blocked by guardrail.",
                blocked=True,
                metadata={**response.metadata, "llm_guard_output": details},
            )
        return TargetResponse(
            content=sanitized,
            blocked=False,
            metadata={
                **response.metadata,
                "llm_guard_output_risk": risk_score,
                "llm_guard_output": details,
            },
        )


def _check_llm_guard_installed():
    """Check if llm-guard is installed."""
    try:
        import llm_guard
        return True
    except ImportError:
        return False


def _load_llm_guard_scan_functions():
    try:
        llm_guard = import_module("llm_guard")
    except ImportError as exc:
        raise RuntimeError("llm-guard is not installed.") from exc

    scan_prompt = getattr(llm_guard, "scan_prompt", None)
    scan_output = getattr(llm_guard, "scan_output", None)
    if not scan_prompt or not scan_output:
        raise RuntimeError("llm-guard scan functions not found.")
    return scan_prompt, scan_output


def _build_scanners(module_path: str, scanner_names: Iterable[str]) -> List[Any]:
    if not scanner_names:
        return []
    module = import_module(module_path)
    scanners: List[Any] = []
    for name in scanner_names:
        scanner_cls = getattr(module, name, None)
        if scanner_cls is None:
            raise RuntimeError(f"LLM Guard scanner not found: {name}")
        scanners.append(scanner_cls())
    return scanners


def _scan_prompt(
    scan_prompt_func, scanners: List[Any], prompt: str
) -> Tuple[str, bool, float, Any]:
    result = scan_prompt_func(scanners, prompt)
    return _normalize_scan_result(result, prompt)


def _scan_output(
    scan_output_func, scanners: List[Any], prompt: str, output: str
) -> Tuple[str, bool, float, Any]:
    result = scan_output_func(scanners, prompt, output)
    return _normalize_scan_result(result, output)


def _normalize_scan_result(result: Any, fallback_text: str) -> Tuple[str, bool, float, Any]:
    if isinstance(result, tuple):
        if len(result) == 3:
            sanitized, is_valid, risk_score = result
            return sanitized, bool(is_valid), float(risk_score), None
        if len(result) >= 4:
            sanitized, is_valid, risk_score, details = result[:4]
            return sanitized, bool(is_valid), float(risk_score), details
    return fallback_text, True, 0.0, None

