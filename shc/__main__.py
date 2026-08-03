"""CLI entry point for the self-healing agent."""

import argparse
import sys


def main() -> None:
    """Main entry point for the shc CLI."""
    parser = argparse.ArgumentParser(
        prog="shc",
        description="Self-Healing Code-Generation Agent",
    )
    subparsers = parser.add_subparsers(dest="command")

    # Run command
    run_parser = subparsers.add_parser("run", help="Execute a repair run")
    run_parser.add_argument("--models", required=True, help="Comma-separated model list")
    run_parser.add_argument("--tiers", default="T0,T1,T2,T3", help="Comma-separated tier list")
    run_parser.add_argument("--seeds", type=int, default=3, help="Number of seeds")
    run_parser.add_argument("--max-attempts", type=int, default=5, help="Max repair attempts")

    # Validate command
    subparsers.add_parser("validate", help="Validate task suite")

    # Reap command
    subparsers.add_parser("reap", help="Remove orphaned shc-* containers")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate metrics report")
    report_parser.add_argument("--run", required=True, help="Run ID")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    if args.command == "run":
        from shc.run import execute_run

        execute_run(
            models=args.models.split(","),
            tiers=args.tiers.split(","),
            seeds=args.seeds,
            max_attempts=args.max_attempts,
        )
    elif args.command == "validate":
        from shc.suite.validate import validate_suite

        validate_suite()
    elif args.command == "reap":
        from shc.sandbox.reaper import reap_all

        reap_all()
    elif args.command == "report":
        from shc.metrics.report import generate_report

        generate_report(args.run)


if __name__ == "__main__":
    main()
