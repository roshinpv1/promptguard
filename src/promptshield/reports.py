from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from promptshield.models import AttackResult, RunArtifacts
from promptshield.utils import write_json


def _attack_result_payload(result: AttackResult) -> Dict[str, Any]:
    return {
        "attack_id": result.attack.attack_id,
        "category": result.attack.category,
        "prompt": result.attack.prompt,
        "source": result.attack.source,
        "attempts": result.attempts,
        "response": {
            "content": result.response.content,
            "blocked": result.response.blocked,
            "metadata": result.response.metadata,
        },
        "judge": {
            "jailbreak_success": result.judge.jailbreak_success,
            "prompt_injection_success": result.judge.prompt_injection_success,
            "pii_leak": result.judge.pii_leak,
            "toxicity_severity": result.judge.toxicity_severity,
            "refusal_quality_failure": result.judge.refusal_quality_failure,
            "notes": result.judge.notes,
        },
        "timestamp": result.timestamp,
    }


def write_reports(artifacts: RunArtifacts, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    attacks_payload: List[Dict[str, Any]] = [
        _attack_result_payload(result) for result in artifacts.results
    ]
    payload = {
        "run_id": artifacts.run_id,
        "model_id": artifacts.model_id,
        "prompt_hash": artifacts.prompt_hash,
        "commit_ref": artifacts.commit_ref,
        "score": {
            "security_score": artifacts.score.security_score,
            "jailbreak_success_rate": artifacts.score.jailbreak_success_rate,
            "prompt_injection_success_rate": artifacts.score.prompt_injection_success_rate,
            "pii_leak_rate": artifacts.score.pii_leak_rate,
            "toxicity_severity": artifacts.score.toxicity_severity,
            "refusal_quality_fail_rate": artifacts.score.refusal_quality_fail_rate,
            "guard_block_rate": artifacts.score.guard_block_rate,
            "guard_false_negative_rate": artifacts.score.guard_false_negative_rate,
            "verdict": artifacts.score.verdict,
            "thresholds": artifacts.score.thresholds,
        },
        "metadata": artifacts.metadata,
        "attacks": attacks_payload,
    }
    write_json(output_dir / "results.json", payload)

