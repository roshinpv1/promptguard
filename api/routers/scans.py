from __future__ import annotations

import yaml
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError

from api.models import (
    ScanRequest, ScanResponse, ScanSummary, ScanListResponse,
    AttackResultResponse, ScoreBreakdownResponse, ErrorResponse
)
from api.tasks import run_scan_async
from promptshield.config import load_config, PromptShieldConfig
from promptshield.models import RunArtifacts

router = APIRouter()

# In-memory storage (replace with database in production)
scan_storage: dict[str, dict] = {}


def _artifacts_to_response(artifacts: RunArtifacts, status: str = "completed") -> ScanResponse:
    """Convert RunArtifacts to API response model."""
    attacks = [
        AttackResultResponse(
            attack_id=result.attack.attack_id,
            category=result.attack.category,
            prompt=result.attack.prompt,
            source=result.attack.source,
            attempts=result.attempts,
            response={
                "content": result.response.content,
                "blocked": result.response.blocked,
                "metadata": result.response.metadata,
            },
            judge={
                "jailbreak_success": result.judge.jailbreak_success,
                "prompt_injection_success": result.judge.prompt_injection_success,
                "pii_leak": result.judge.pii_leak,
                "toxicity_severity": result.judge.toxicity_severity,
                "refusal_quality_failure": result.judge.refusal_quality_failure,
                "notes": result.judge.notes,
            },
            timestamp=result.timestamp,
        )
        for result in artifacts.results
    ]
    
    score = ScoreBreakdownResponse(
        security_score=artifacts.score.security_score,
        jailbreak_success_rate=artifacts.score.jailbreak_success_rate,
        prompt_injection_success_rate=artifacts.score.prompt_injection_success_rate,
        pii_leak_rate=artifacts.score.pii_leak_rate,
        toxicity_severity=artifacts.score.toxicity_severity,
        refusal_quality_fail_rate=artifacts.score.refusal_quality_fail_rate,
        guard_block_rate=artifacts.score.guard_block_rate,
        guard_false_negative_rate=artifacts.score.guard_false_negative_rate,
        verdict=artifacts.score.verdict,
        thresholds=artifacts.score.thresholds,
    )
    
    return ScanResponse(
        run_id=artifacts.run_id,
        model_id=artifacts.model_id,
        prompt_hash=artifacts.prompt_hash,
        commit_ref=artifacts.commit_ref,
        score=score,
        metadata=artifacts.metadata,
        attacks=attacks,
        status=status,
        created_at=artifacts.metadata.get("generated_at", datetime.utcnow().isoformat() + "Z"),
    )


@router.post("/scans", response_model=ScanResponse, status_code=201)
async def create_scan(request: ScanRequest):
    """
    Start a new PromptShield scan.
    
    Accepts either:
    - config: JSON config object
    - config_yaml: YAML config string
    - system_prompt: System prompt content (will create temp file)
    """
    try:
        # Load config
        if request.config_yaml:
            import tempfile
            from pathlib import Path
            with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                f.write(request.config_yaml)
                config_path = f.name
            config_dict = yaml.safe_load(request.config_yaml)
            Path(config_path).unlink(missing_ok=True)
        elif request.config:
            config_dict = request.config
        else:
            # Use default config
            from promptshield.config import load_config
            default_config = load_config("promptshield.yaml")
            config_dict = {
                "version": default_config.version,
                "run": {
                    "seed": default_config.run.seed,
                    "worst_of_n": default_config.run.worst_of_n,
                    "output_dir": default_config.run.output_dir,
                    "prompt_path": default_config.run.prompt_path,
                },
                "target": {
                    "type": default_config.target.type,
                    "model_id": default_config.target.model_id,
                    "behavior": default_config.target.behavior,
                },
                "guard": {
                    "enabled": default_config.guard.enabled,
                    "type": default_config.guard.type,
                    "block_on_patterns": default_config.guard.block_on_patterns,
                    "input_scanners": default_config.guard.input_scanners,
                    "output_scanners": default_config.guard.output_scanners,
                },
                "judge": {
                    "type": default_config.judge.type,
                    "toxicity_terms": default_config.judge.toxicity_terms,
                },
                "scoring": {
                    "weights": default_config.scoring.weights,
                    "thresholds": default_config.scoring.thresholds,
                },
                "attacks": {
                    "garak": default_config.attacks.garak,
                    "pyrit": default_config.attacks.pyrit,
                },
            }
        
        # Run scan
        artifacts = await run_scan_async(config_dict, request.system_prompt)
        
        # Store results
        response = _artifacts_to_response(artifacts)
        scan_storage[artifacts.run_id] = {
            "artifacts": artifacts,
            "response": response,
            "created_at": response.created_at,
        }
        
        return response
        
    except Exception as e:
        import traceback
        error_detail = f"Scan failed: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)  # Log for debugging
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


@router.get("/scans", response_model=ScanListResponse)
async def list_scans(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """List all scans with pagination."""
    scans_list = list(scan_storage.values())
    total = len(scans_list)
    
    # Sort by created_at descending
    scans_list.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Paginate
    start = (page - 1) * page_size
    end = start + page_size
    paginated = scans_list[start:end]
    
    summaries = [
        ScanSummary(
            run_id=item["response"].run_id,
            model_id=item["response"].model_id,
            verdict=item["response"].score.verdict,
            security_score=item["response"].score.security_score,
            status=item["response"].status,
            created_at=item["created_at"],
        )
        for item in paginated
    ]
    
    return ScanListResponse(
        scans=summaries,
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/scans/{run_id}", response_model=ScanResponse)
async def get_scan(run_id: str):
    """Get scan details by run_id."""
    if run_id not in scan_storage:
        raise HTTPException(status_code=404, detail=f"Scan {run_id} not found")
    
    return scan_storage[run_id]["response"]


@router.get("/scans/{run_id}/results", response_model=dict)
async def get_scan_results(run_id: str):
    """Get full scan results as JSON."""
    if run_id not in scan_storage:
        raise HTTPException(status_code=404, detail=f"Scan {run_id} not found")
    
    artifacts = scan_storage[run_id]["artifacts"]
    
    # Convert to dict matching the JSON report format
    attacks_payload = [
        {
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
        for result in artifacts.results
    ]
    
    return {
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


@router.delete("/scans/{run_id}", status_code=204)
async def delete_scan(run_id: str):
    """Delete a scan."""
    if run_id not in scan_storage:
        raise HTTPException(status_code=404, detail=f"Scan {run_id} not found")
    
    del scan_storage[run_id]
    return None

