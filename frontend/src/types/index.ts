export interface ScanRequest {
  config?: Record<string, any>;
  config_yaml?: string;
  system_prompt?: string;
}

export interface AttackResultResponse {
  attack_id: string;
  category: string;
  prompt: string;
  source: string;
  attempts: number;
  response: {
    content: string;
    blocked: boolean;
    metadata: Record<string, any>;
  };
  judge: {
    jailbreak_success: boolean;
    prompt_injection_success: boolean;
    pii_leak: boolean;
    toxicity_severity: number;
    refusal_quality_failure: boolean;
    notes: string[];
  };
  timestamp: string;
}

export interface ScoreBreakdownResponse {
  security_score: number;
  jailbreak_success_rate: number;
  prompt_injection_success_rate: number;
  pii_leak_rate: number;
  toxicity_severity: number;
  refusal_quality_fail_rate: number;
  guard_block_rate: number;
  guard_false_negative_rate: number;
  verdict: "PASS" | "WARN" | "FAIL";
  thresholds: {
    pass: number;
    warn: number;
  };
}

export interface ScanResponse {
  run_id: string;
  model_id: string;
  prompt_hash: string | null;
  commit_ref: string | null;
  score: ScoreBreakdownResponse;
  metadata: Record<string, any>;
  attacks: AttackResultResponse[];
  status: string;
  created_at: string;
}

export interface ScanSummary {
  run_id: string;
  model_id: string;
  verdict: string;
  security_score: number;
  status: string;
  created_at: string;
}

export interface ScanListResponse {
  scans: ScanSummary[];
  total: number;
  page: number;
  page_size: number;
}

export interface TestAPIRequest {
  api_url: string;
  api_key?: string;
  model_id: string;
  system_prompt: string;
  api_type?: string;
  headers?: Record<string, string>;
  config_overrides?: Record<string, any>;
}

export interface TestAPIResponse {
  run_id: string;
  verdict: string;
  security_score: number;
  score_breakdown: ScoreBreakdownResponse;
  results: AttackResultResponse[];
  metadata: Record<string, any>;
}

export interface ConfigResponse {
  config: Record<string, any>;
  default: boolean;
}

export interface ConfigUpdateRequest {
  config: Record<string, any>;
}

