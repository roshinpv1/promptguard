from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import json
from pathlib import Path

from promptguard.models import SecurityReport


def write_report(report: SecurityReport, output_dir: Path) -> None:
    """Write security report to JSON file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    payload = {
        "report_id": report.report_id,
        "model_id": report.model_id,
        "prompt_hash": report.prompt_hash,
        "commit_ref": report.commit_ref,
        "policy_id": report.policy_id,
        "decision": {
            "policy_id": report.decision.policy_id,
            "verdict": report.decision.verdict,
            "risk_score": report.decision.risk_score,
            "explanation": report.decision.explanation,
            "findings_count": len(report.decision.findings),
        },
        "findings": [
            {
                "finding_id": f.finding_id,
                "category": f.category,
                "severity": f.severity.value,
                "risk_score": f.risk_score,
                "title": f.title,
                "description": f.description,
                "evidence": f.evidence,
                "root_cause": f.root_cause,
                "remediation": f.remediation,
            }
            for f in report.findings
        ],
        "probe_results": [
            {
                "probe_id": r.probe_id,
                "risk_score": r.risk_score,
                "severity": r.severity.value,
                "blocked": r.blocked,
                "evidence": r.evidence,
            }
            for r in report.probe_results
        ],
        "metadata": report.metadata,
        "generated_at": report.generated_at,
    }
    
    report_path = output_dir / "security_report.json"
    report_path.write_text(json.dumps(payload, indent=2))

