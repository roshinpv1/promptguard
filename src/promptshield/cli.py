from __future__ import annotations

import argparse
import sys

from promptshield.config import load_config
from promptshield.runner import run_scan


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="promptshield")
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan", help="Run PromptShield scan")
    scan_parser.add_argument(
        "--config",
        default="promptshield.yaml",
        help="Path to config file",
    )
    scan_parser.add_argument(
        "--output-dir",
        default=None,
        help="Override output directory",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command != "scan":
        parser.print_help()
        return 1

    config = load_config(args.config)
    if args.output_dir:
        config.run.output_dir = args.output_dir

    artifacts = run_scan(config)
    verdict = artifacts.score.verdict
    score = artifacts.score.security_score
    print(f"PromptShield verdict: {verdict} (score={score:.2f})")
    return 0 if verdict == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())

