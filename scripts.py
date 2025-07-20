#!/usr/bin/env python3
"""Project scripts for common tasks."""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str) -> int:
    """Run a shell command and return exit code."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode


def format_code():
    """Format code with ruff."""
    return run_command("ruff format")


def lint_code():
    """Lint code with ruff."""
    return run_command("ruff check")


def typecheck():
    """Run type checking with basedpyright."""
    return run_command("basedpyright")


def check_all():
    """Run all checks: lint and typecheck."""
    lint_result = lint_code()
    if lint_result != 0:
        return lint_result
    return typecheck()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python scripts.py <command>")
        print("Commands: format, lint, typecheck, check")
        return 1

    command = sys.argv[1]

    commands = {
        "format": format_code,
        "lint": lint_code,
        "typecheck": typecheck,
        "check": check_all,
    }

    if command not in commands:
        print(f"Unknown command: {command}")
        print(f"Available commands: {', '.join(commands.keys())}")
        return 1

    return commands[command]()


if __name__ == "__main__":
    sys.exit(main())
