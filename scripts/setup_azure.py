#!/usr/bin/env python3
"""
Azure Workshop Setup Script

Configures Azure region for workshop deployment.
Cleans stale Azure config from .env while preserving Neo4j settings.

Prerequisites:
    az login --use-device-code
    azd auth login --use-device-code

Usage:
    uv run python scripts/setup_azure.py
    uv run python scripts/setup_azure.py --region westus
    uv run python scripts/setup_azure.py --env production
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def clean_env_file(env_path: Path) -> None:
    """Clean stale Azure config from .env while preserving Neo4j settings."""
    if not env_path.exists():
        return

    # Read all lines
    with open(env_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Check if there are Azure/Service settings to clean
    has_azure_config = any(
        line.strip().startswith(("AZURE_", "SERVICE_", "EMBEDDING_"))
        for line in lines
        if not line.strip().startswith("#")
    )

    if not has_azure_config:
        return

    print()
    print("Found existing Azure configuration in .env that may conflict with new deployment.")

    # Extract Neo4j settings
    neo4j_lines = [
        line for line in lines
        if line.strip().startswith("NEO4J_") and not line.strip().startswith("#")
    ]

    if neo4j_lines:
        # Rebuild .env with only Neo4j settings
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("# ============================================\n")
            f.write("# User Configuration\n")
            f.write("# ============================================\n")
            f.write("# Neo4j Connection (configure these manually)\n")
            f.write("\n")
            f.writelines(neo4j_lines)

        print("Removed stale Azure config from .env (Neo4j settings preserved)")
    else:
        # No Neo4j settings, remove Azure config only
        filtered_lines = [
            line for line in lines
            if not line.strip().startswith(("AZURE_", "SERVICE_", "EMBEDDING_"))
            or line.strip().startswith("#")
        ]

        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(filtered_lines)

        print("Cleaned stale Azure configuration from .env...")
        print("Done")


def remove_azure_directory(azure_dir: Path) -> None:
    """Remove existing .azure directory to start fresh."""
    if azure_dir.exists():
        print("Removing existing .azure directory...")
        shutil.rmtree(azure_dir)


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=True,
            text=True,
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {' '.join(cmd)}")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        raise


def initialize_azd_environment(env_name: str, region: str) -> None:
    """Initialize azd environment and set region."""
    print("Initializing azd environment...")

    # Initialize new azd environment
    run_command(["azd", "init", "-e", env_name])

    # Set Azure location
    run_command(["azd", "env", "set", "AZURE_LOCATION", region])


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Configure Azure region for workshop deployment"
    )
    parser.add_argument(
        "--region",
        "-r",
        default="eastus2",
        help="Azure region to use (default: eastus2)",
    )
    parser.add_argument(
        "--env",
        "-e",
        default="workshop",
        help="Azure environment name (default: workshop)",
    )
    args = parser.parse_args()

    project_root = get_project_root()
    env_path = project_root / ".env"
    azure_dir = project_root / ".azure"

    print()
    print(f"Using Azure region: {args.region}")

    try:
        # Clean stale Azure config from .env before azd init
        clean_env_file(env_path)

        # Remove existing azd environment to start fresh
        remove_azure_directory(azure_dir)

        # Initialize new azd environment
        initialize_azd_environment(args.env, args.region)

        print()
        print(f"Azure configured: {args.region}")
        print()
        print("Ready to deploy! Run:")
        print("   azd up")
        return 0

    except subprocess.CalledProcessError:
        print()
        print("Error: Failed to configure Azure environment")
        print()
        print("Make sure you have run:")
        print("   az login --use-device-code")
        print("   azd auth login --use-device-code")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
