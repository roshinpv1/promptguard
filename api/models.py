from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# Request Models
class ScanRequest(BaseModel):
    config: Optional[Dict[str, Any]] = None
    config_yaml: Optional[str] = None
    system_prompt: Optional[str] = None


class TestAPIRequest(BaseModel):
    api_url: str = Field(..., description="External LLM API endpoint URL")
    api_key: Optional[str] = Field(None, description="API key for authentication")
    model_id: str = Field(..., description="Model identifier")
    system_prompt: str = Field(..., description="System prompt to test")
    api_type: str = Field("openai", description="API type: openai, anthropic, azure, custom")
    headers: Optional[Dict[str, str]] = Field(None, description="Custom headers")
    config_overrides: Optional[Dict[str, Any]] = Field(None, description="Config overrides")


class ConfigUpdateRequest(BaseModel):
    config: Dict[str, Any]


# Response Models
class AttackResultResponse(BaseModel):
    attack_id: str
    category: str
    prompt: str
    source: str
    attempts: int
    response: Dict[str, Any]
    judge: Dict[str, Any]
    timestamp: str


class ScoreBreakdownResponse(BaseModel):
    security_score: float
    jailbreak_success_rate: float
    prompt_injection_success_rate: float
    pii_leak_rate: float
    toxicity_severity: float
    refusal_quality_fail_rate: float
    guard_block_rate: float
    guard_false_negative_rate: float
    verdict: str
    thresholds: Dict[str, float]


class ScanResponse(BaseModel):
    run_id: str
    model_id: str
    prompt_hash: Optional[str]
    commit_ref: Optional[str]
    score: ScoreBreakdownResponse
    metadata: Dict[str, Any]
    attacks: List[AttackResultResponse]
    status: str = "completed"
    created_at: str


class ScanSummary(BaseModel):
    run_id: str
    model_id: str
    verdict: str
    security_score: float
    status: str
    created_at: str


class ScanListResponse(BaseModel):
    scans: List[ScanSummary]
    total: int
    page: int = 1
    page_size: int = 20


class TestAPIResponse(BaseModel):
    run_id: str
    verdict: str
    security_score: float
    score_breakdown: ScoreBreakdownResponse
    results: List[AttackResultResponse]
    metadata: Dict[str, Any]


class ConfigResponse(BaseModel):
    config: Dict[str, Any]
    default: bool = False


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

