from __future__ import annotations

import random
import uuid
from typing import List, Tuple

from promptshield.config import PromptShieldConfig
from promptshield.engines.garak_engine import build_garak_attacks
from promptshield.engines.pyrit_engine import build_pyrit_attacks
from promptshield.guard.base import Guard
from promptshield.guard.llm_guard import PatternGuard
from promptshield.integrations.llm_guard_adapter import LLMGuardAdapter
from promptshield.judge.safety_judge import SafetyJudge
from promptshield.models import Attack, AttackResult, RunArtifacts, TargetResponse
from promptshield.reports import write_reports
from promptshield.scoring import compute_score
from promptshield.targets.mock import MockTarget
from promptshield.utils import current_commit_ref, ensure_dir, sha256_file, utc_now


def _load_target(config: PromptShieldConfig) -> MockTarget:
    return MockTarget(config.target.behavior, seed=config.run.seed)


def _build_attacks(config: PromptShieldConfig) -> List[Attack]:
    attacks: List[Attack] = []
    garak_cfg = config.attacks.garak or {}
    if garak_cfg.get("enabled", True):
        probes = garak_cfg.get("probes", [])
        use_library = garak_cfg.get("mode", "builtin") == "library"
        attacks.extend(build_garak_attacks(probes, use_library=use_library))

    pyrit_cfg = config.attacks.pyrit or {}
    if pyrit_cfg.get("enabled", True):
        base_prompts = pyrit_cfg.get("base_prompts", [])
        mutations = pyrit_cfg.get("mutations", [])
        use_library = pyrit_cfg.get("mode", "builtin") == "library"
        generator_path = pyrit_cfg.get("generator")
        attacks.extend(
            build_pyrit_attacks(
                base_prompts,
                mutations,
                use_library=use_library,
                generator_path=generator_path,
            )
        )

    return attacks


def _run_attack(
    attack: Attack,
    target: Target,
    guard: Guard | None,
    judge: SafetyJudge,
    attempts: int,
    seed: int,
) -> AttackResult:
    rng = random.Random(seed)
    best_result: AttackResult | None = None
    for idx in range(attempts):
        rng.seed(seed + idx)
        prompt = attack.prompt
        if guard:
            input_decision = guard.scan_input(prompt)
            prompt = input_decision.prompt
            if input_decision.blocked:
                response = TargetResponse(
                    content=input_decision.reason or "Request blocked by guardrail.",
                    blocked=True,
                    metadata=input_decision.metadata,
                )
                guarded = response
                judge_result = judge.evaluate(attack, guarded)
                current = AttackResult(
                    attack=attack,
                    response=guarded,
                    judge=judge_result,
                    attempts=attempts,
                )
                if not best_result or current.judge.risk_score() > best_result.judge.risk_score():
                    best_result = current
                continue

        if isinstance(target, APITarget):
            response_content = target.generate_sync(prompt)
            response = TargetResponse(content=response_content, blocked=False)
        else:
            response = target.generate(prompt)
        guarded = guard.scan_output(attack.prompt, response) if guard else response
        judge_result = judge.evaluate(attack, guarded)
        current = AttackResult(
            attack=attack,
            response=guarded,
            judge=judge_result,
            attempts=attempts,
        )
        if not best_result or current.judge.risk_score() > best_result.judge.risk_score():
            best_result = current
    return best_result


def _load_guard(config: PromptShieldConfig) -> Guard | None:
    if not config.guard.enabled:
        return None
    if config.guard.type == "llm_guard":
        try:
            return LLMGuardAdapter(
                input_scanners=config.guard.input_scanners,
                output_scanners=config.guard.output_scanners,
            )
        except ImportError as e:
            # Fallback to pattern guard if llm-guard is not installed
            print(f"Warning: {e}")
            print("Falling back to pattern-based guard.")
            return PatternGuard(config.guard.block_on_patterns)
    return PatternGuard(config.guard.block_on_patterns)


def run_scan(config: PromptShieldConfig) -> RunArtifacts:
    run_id = uuid.uuid4().hex
    prompt_hash = sha256_file(config.run.prompt_path)
    commit_ref = current_commit_ref()

    target = _load_target(config)
    guard = _load_guard(config)
    judge = SafetyJudge(config.judge.toxicity_terms)

    attacks = _build_attacks(config)
    results: List[AttackResult] = []
    guard_blocks = 0
    guard_false_negatives = 0

    for attack in attacks:
        result = _run_attack(
            attack=attack,
            target=target,
            guard=guard,
            judge=judge,
            attempts=config.run.worst_of_n,
            seed=config.run.seed,
        )
        if result.response.blocked:
            guard_blocks += 1
        if not result.response.blocked and result.judge.risk_score() > 0:
            guard_false_negatives += 1
        results.append(result)

    score = compute_score(
        results=results,
        weights=config.scoring.weights,
        thresholds=config.scoring.thresholds,
        guard_stats=(guard_blocks, guard_false_negatives),
    )

    artifacts = RunArtifacts(
        run_id=run_id,
        model_id=config.target.model_id,
        prompt_hash=prompt_hash,
        commit_ref=commit_ref,
        results=results,
        score=score,
        metadata={"generated_at": utc_now()},
    )

    output_dir = ensure_dir(config.run.output_dir)
    write_reports(artifacts, output_dir)
    return artifacts

