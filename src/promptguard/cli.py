from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from promptguard.runner import run_security_assessment
from promptguard.reports import write_report
from promptshield.config import load_config


def main(argv: list[str] | None = None) -> int:
    """CLI entrypoint for PromptGuard."""
    parser = argparse.ArgumentParser(prog="promptguard")
    parser.add_argument(
        "command",
        choices=["assess", "scan"],  # 'scan' for backward compatibility
        help="Command to run",
    )
    parser.add_argument(
        "--config",
        default="promptshield.yaml",
        help="Path to config file",
    )
    parser.add_argument(
        "--policy",
        help="Path to policy YAML file",
    )
    parser.add_argument(
        "--output-dir",
        default="artifacts",
        help="Output directory for reports",
    )
    
    args = parser.parse_args(argv)
    
    # Load config
    config = load_config(args.config)
    
    # Run assessment
    report = run_security_assessment(config, args.policy)
    
    # Write report
    output_dir = Path(args.output_dir)
    write_report(report, output_dir)
    
    # Print verdict
    verdict = report.decision.verdict
    score = report.decision.risk_score
    print(f"PromptGuard verdict: {verdict} (risk_score={score:.2f})")
    print(f"Findings: {len(report.findings)}")
    
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())

