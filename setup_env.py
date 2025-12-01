import subprocess
import os
import sys
from pathlib import Path

# Variables that are auto-generated from azd (will be updated/overwritten)
AZD_MANAGED_VARS = {
    'AZURE_AI_PROJECT_ENDPOINT',
    'AZURE_AI_MODEL_NAME',
    'AZURE_AI_EMBEDDING_NAME',
    'AZURE_OPENAI_ENDPOINT',
    'AZURE_AI_AGENT_NAME',
    'AZURE_TENANT_ID',
    'AZURE_RESOURCE_GROUP',
    'AZURE_CONTAINER_ENVIRONMENT_NAME',
    'AZURE_CONTAINER_REGISTRY_ENDPOINT',
    'SERVICE_API_IDENTITY_PRINCIPAL_ID',
    'SERVICE_API_NAME',
    'SERVICE_API_URI',
    'SERVICE_API_ENDPOINTS',
}

ENV_FILE = Path('.env')
SAMPLE_FILE = Path('.env.sample')


def parse_env_file(filepath: Path) -> dict[str, str]:
    """Parse a .env file into a dictionary, preserving only KEY=VALUE lines."""
    env_vars = {}
    if not filepath.exists():
        return env_vars

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            # Parse KEY=VALUE (handle values with = in them)
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


def main():
    print("Fetching environment variables from 'azd'...")

    try:
        # Run azd env get-values
        result = subprocess.run(
            ["azd", "env", "get-values"],
            capture_output=True,
            text=True,
            check=True
        )

        azd_vars = parse_azd_output(result.stdout)

        # Filter to only the variables we want to sync
        azd_managed = {k: v for k, v in azd_vars.items() if k in AZD_MANAGED_VARS}

        if ENV_FILE.exists():
            # Read existing .env preserving structure
            lines, var_positions = read_env_with_structure(ENV_FILE)
            existing_vars = parse_env_file(ENV_FILE)

            # Update existing azd-managed variables in place
            updated_vars = set()
            for var_name, value in azd_managed.items():
                if var_name in var_positions:
                    # Update in place
                    line_idx = var_positions[var_name]
                    lines[line_idx] = f'{var_name}={value}'
                    updated_vars.add(var_name)

            # Append new azd-managed variables that don't exist
            new_vars = set(azd_managed.keys()) - updated_vars
            if new_vars:
                # Add a blank line if the file doesn't end with one
                if lines and lines[-1].strip():
                    lines.append('')
                for var_name in sorted(new_vars):
                    lines.append(f'{var_name}={azd_managed[var_name]}')

            # Write back
            with open(ENV_FILE, 'w') as f:
                f.write('\n'.join(lines))
                if lines:
                    f.write('\n')

            print(f"Updated '{ENV_FILE}'")

        else:
            # No existing .env - create from sample if it exists, otherwise create minimal
            if SAMPLE_FILE.exists():
                lines, var_positions = read_env_with_structure(SAMPLE_FILE)

                # Update azd-managed variables in the sample
                for var_name, value in azd_managed.items():
                    if var_name in var_positions:
                        line_idx = var_positions[var_name]
                        lines[line_idx] = f'{var_name}={value}'
                    else:
                        lines.append(f'{var_name}={value}')

                with open(ENV_FILE, 'w') as f:
                    f.write('\n'.join(lines))
                    if lines:
                        f.write('\n')
            else:
                # Create minimal .env with just azd vars
                with open(ENV_FILE, 'w') as f:
                    f.write("# Auto-generated by setup_env.py (from azd)\n")
                    for key in sorted(azd_managed.keys()):
                        f.write(f'{key}={azd_managed[key]}\n')

            print(f"Created '{ENV_FILE}'")

        # Show key variables that were set
        print("\nAzure variables synced:")
        for key in ['AZURE_AI_PROJECT_ENDPOINT', 'AZURE_AI_MODEL_NAME',
                    'AZURE_AI_EMBEDDING_NAME', 'AZURE_OPENAI_ENDPOINT']:
            if key in azd_managed:
                value = azd_managed[key]
                # Truncate long values
                if len(value) > 50:
                    value = value[:47] + "..."
                print(f"  {key}={value}")

        print("\nYou can now run the application:")
        print("  uv run uvicorn api.main:create_app --factory --reload")

    except FileNotFoundError:
        print("Error: 'azd' command not found. Please install Azure Developer CLI.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: Failed to get azd environment values.")
        print("  Ensure you have run 'azd up' or 'azd env new' in this directory.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
