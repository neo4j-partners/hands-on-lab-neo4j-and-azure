"""
Sync Azure deployment outputs to .env file.

Run after 'azd up' to populate environment variables.
"""

import subprocess
import sys
from pathlib import Path

# Variables synced from azd deployment outputs
AZD_MANAGED_VARS = {
    'AZURE_AI_PROJECT_ENDPOINT',
    'AZURE_AI_SERVICES_ENDPOINT',
    'AZURE_AI_MODEL_NAME',
    'AZURE_AI_EMBEDDING_NAME',
    'AZURE_TENANT_ID',
    'AZURE_RESOURCE_GROUP',
}

# Variables that should NEVER be modified by this script (user-managed)
PROTECTED_VARS = {
    # Neo4j Connection
    'NEO4J_URI',
    'NEO4J_USERNAME',
    'NEO4J_PASSWORD',
}

# Placeholder templates for variables that need user configuration
PLACEHOLDER_SECTIONS = {
    'neo4j': {
        'header': '# Neo4j Database Connection',
        'vars': [
            ('NEO4J_URI', 'neo4j+s://xxx.databases.neo4j.io'),
            ('NEO4J_USERNAME', 'neo4j'),
            ('NEO4J_PASSWORD', 'your-password'),
        ]
    },
}

ENV_FILE = Path('.env')


def parse_env_file(filepath: Path) -> dict[str, str]:
    """Parse a .env file into a dictionary, preserving only KEY=VALUE lines."""
    env_vars = {}
    if not filepath.exists():
        return env_vars

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, _, value = line.partition('=')
                key = key.strip()
                value = value.strip().strip('"')
                if key:
                    env_vars[key] = value
    return env_vars


def parse_azd_output(output: str) -> dict[str, str]:
    """Parse azd env get-values output into a dictionary."""
    env_vars = {}
    for line in output.strip().split('\n'):
        if '=' in line:
            key, _, value = line.partition('=')
            key = key.strip()
            value = value.strip().strip('"')
            if key:
                env_vars[key] = value
    return env_vars


def read_env_with_structure(filepath: Path) -> tuple[list[str], dict[str, int]]:
    """
    Read .env file preserving structure.
    Returns (lines, var_positions) where var_positions maps var names to line indices.
    """
    lines = []
    var_positions = {}

    if not filepath.exists():
        return lines, var_positions

    with open(filepath, 'r') as f:
        for i, line in enumerate(f):
            lines.append(line.rstrip('\n'))
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and '=' in stripped:
                key = stripped.partition('=')[0].strip()
                var_positions[key] = i

    return lines, var_positions


def add_placeholder_sections(lines: list[str], existing_vars: dict[str, str]) -> list[str]:
    """
    Add placeholder sections for missing variables.
    Does not overwrite existing variables.
    """
    for section in PLACEHOLDER_SECTIONS.values():
        # Check if any vars from this section are missing
        missing_vars = [
            (name, default) for name, default in section['vars']
            if name not in existing_vars
        ]

        if missing_vars:
            # Add section header and missing vars
            if lines and lines[-1].strip():
                lines.append('')
            lines.append(section['header'])
            for var_name, default_value in missing_vars:
                lines.append(f'{var_name}={default_value}')

    return lines


def main():
    print("Syncing environment configuration...")

    try:
        # Get azd deployment outputs
        print("\n1. Fetching Azure AI configuration from 'azd'...")
        result = subprocess.run(
            ["azd", "env", "get-values"],
            capture_output=True,
            text=True,
            check=True
        )

        azd_vars = parse_azd_output(result.stdout)

        # Filter to only the variables we want to sync
        azd_managed = {
            k: v for k, v in azd_vars.items()
            if k in AZD_MANAGED_VARS and k not in PROTECTED_VARS
        }

        if ENV_FILE.exists():
            lines, var_positions = read_env_with_structure(ENV_FILE)
            existing_vars = parse_env_file(ENV_FILE)

            # Update existing managed variables in place
            updated_vars = set()
            for var_name, value in azd_managed.items():
                if var_name in var_positions:
                    line_idx = var_positions[var_name]
                    lines[line_idx] = f'{var_name}={value}'
                    updated_vars.add(var_name)

            # Append new azd-managed variables that don't exist
            new_azd_vars = set(azd_managed.keys()) - updated_vars
            if new_azd_vars:
                if lines and lines[-1].strip():
                    lines.append('')
                lines.append('# Azure AI (from azd)')
                for var_name in sorted(new_azd_vars):
                    lines.append(f'{var_name}={azd_managed[var_name]}')
                    existing_vars[var_name] = azd_managed[var_name]

            # Add placeholders for missing Neo4j variables
            lines = add_placeholder_sections(lines, existing_vars)

            with open(ENV_FILE, 'w') as f:
                f.write('\n'.join(lines))
                if lines:
                    f.write('\n')

            print(f"\n2. Updated '{ENV_FILE}'")

        else:
            # No existing .env - create new with all vars and placeholders
            lines = ['# Auto-generated by setup_env.py', '']

            # Add azd-managed variables
            if azd_managed:
                lines.append('# Azure AI (from azd)')
                for key in sorted(azd_managed.keys()):
                    lines.append(f'{key}={azd_managed[key]}')

            # Add all placeholder sections
            existing_vars = dict(azd_managed)
            lines = add_placeholder_sections(lines, existing_vars)

            with open(ENV_FILE, 'w') as f:
                f.write('\n'.join(lines))
                if lines:
                    f.write('\n')

            print(f"\n2. Created '{ENV_FILE}'")

        # Show synced variables
        print("\nAzure AI configuration:")
        for key in ['AZURE_AI_SERVICES_ENDPOINT', 'AZURE_AI_MODEL_NAME', 'AZURE_AI_EMBEDDING_NAME']:
            if key in azd_managed:
                value = azd_managed[key]
                if len(value) > 50:
                    value = value[:47] + "..."
                print(f"  {key}={value}")

        # Check Neo4j configuration
        final_vars = parse_env_file(ENV_FILE)
        neo4j_uri = final_vars.get('NEO4J_URI', '')
        neo4j_configured = neo4j_uri.startswith('neo4j') and 'xxx' not in neo4j_uri

        print("\nNeo4j configuration:")
        if neo4j_configured:
            print(f"  NEO4J_URI={neo4j_uri[:40]}..." if len(neo4j_uri) > 40 else f"  NEO4J_URI={neo4j_uri}")
        else:
            print("  NEO4J_URI=<placeholder - update with your credentials>")

        # Remind about next steps
        if not neo4j_configured:
            print("\nNext steps:")
            print("  1. Update Neo4j credentials in .env")
            print("  2. Run: uv run python main.py")
        else:
            print("\nReady to run!")
            print("  uv run python main.py")

    except FileNotFoundError:
        print("Error: 'azd' command not found. Please install Azure Developer CLI.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: Failed to get azd environment values.")
        print("  Ensure you have run 'azd up' in this directory.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
